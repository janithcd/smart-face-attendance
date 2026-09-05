import cv2
import mediapipe as mp
import math
import time
from pathlib import Path


# =========================================================
# CONFIGURATION
# =========================================================

LANDMARKER_MODEL = Path("models/face_landmarker.task")

# Blink blendshape thresholds
BLINK_CLOSED_THRESHOLD = 0.55
BLINK_OPEN_THRESHOLD = 0.25
MIN_CLOSED_FRAMES = 2

# Head movement
HEAD_TURN_THRESHOLD = 0.07
RETURN_CENTER_THRESHOLD = 0.035

# Number of frames used to learn the user's straight position
BASELINE_FRAMES = 30


# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def distance(point1, point2):
    return math.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
    )


def calculate_head_position(landmarks):
    """
    Estimate horizontal head orientation.

    234 = left side of face
    454 = right side of face
    1   = nose tip
    """

    left_side = landmarks[234].x
    right_side = landmarks[454].x
    nose = landmarks[1].x

    face_width = right_side - left_side

    if abs(face_width) < 0.0001:
        return 0.5

    return (nose - left_side) / face_width


def get_blendshape_score(blendshapes, category_name):
    """
    Find a blendshape score such as:
    eyeBlinkLeft
    eyeBlinkRight
    """

    for category in blendshapes:

        if category.category_name == category_name:
            return category.score

    return 0.0


# =========================================================
# MAIN LIVENESS TEST
# =========================================================

def run_liveness_test():

    if not LANDMARKER_MODEL.exists():
        print(
            f"Error: Face Landmarker model not found: "
            f"{LANDMARKER_MODEL}"
        )
        return

    # MediaPipe Tasks API
    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = (
        mp.tasks.vision.FaceLandmarkerOptions
    )
    RunningMode = mp.tasks.vision.RunningMode

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(
            model_asset_path=str(LANDMARKER_MODEL)
        ),
        running_mode=RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.6,
        min_face_presence_confidence=0.6,
        min_tracking_confidence=0.6,
        output_face_blendshapes=True
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    # -----------------------------
    # Liveness state
    # -----------------------------

    state = "CALIBRATING"

    baseline_samples = []
    baseline_head_position = None

    closed_frames = 0
    eyes_were_closed = False

    blink_completed = False
    head_turn_completed = False
    liveness_passed = False

    last_timestamp = 0

    print("=" * 50)
    print("          LIVENESS DETECTION TEST")
    print("=" * 50)
    print()
    print("1. Look straight at the camera")
    print("2. Blink when requested")
    print("3. Turn your head when requested")
    print("4. Return to center")
    print()
    print("Press Q to exit.")
    print()

    with FaceLandmarker.create_from_options(
            options
    ) as landmarker:

        while True:

            success, frame = camera.read()

            if not success:
                print("Error: Could not read webcam.")
                break

            # Mirror webcam
            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # Convert OpenCV image into MediaPipe Image
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            # VIDEO mode requires increasing timestamps
            timestamp_ms = int(
                time.perf_counter() * 1000
            )

            if timestamp_ms <= last_timestamp:
                timestamp_ms = last_timestamp + 1

            last_timestamp = timestamp_ms

            result = landmarker.detect_for_video(
                mp_image,
                timestamp_ms
            )

            instruction = "Show your face"

            blink_left = 0.0
            blink_right = 0.0
            head_delta = 0.0

            # =================================================
            # FACE FOUND
            # =================================================

            if (
                    result.face_landmarks
                    and result.face_blendshapes
            ):

                landmarks = result.face_landmarks[0]

                blendshapes = (
                    result.face_blendshapes[0]
                )

                blink_left = get_blendshape_score(
                    blendshapes,
                    "eyeBlinkLeft"
                )

                blink_right = get_blendshape_score(
                    blendshapes,
                    "eyeBlinkRight"
                )

                average_blink = (
                                        blink_left + blink_right
                                ) / 2.0

                head_position = (
                    calculate_head_position(
                        landmarks
                    )
                )

                # =============================================
                # STATE 1 - CALIBRATION
                # =============================================

                if state == "CALIBRATING":

                    instruction = (
                        "LOOK STRAIGHT AT CAMERA"
                    )

                    baseline_samples.append(
                        head_position
                    )

                    if (
                            len(baseline_samples)
                            >= BASELINE_FRAMES
                    ):

                        baseline_head_position = (
                                sum(baseline_samples)
                                / len(baseline_samples)
                        )

                        state = "WAIT_BLINK"

                        print(
                            "Calibration complete."
                        )

                        print(
                            "Please BLINK once."
                        )

                # =============================================
                # STATE 2 - BLINK
                # =============================================

                elif state == "WAIT_BLINK":

                    instruction = "BLINK ONCE"

                    if (
                            average_blink
                            >= BLINK_CLOSED_THRESHOLD
                    ):

                        closed_frames += 1

                        if (
                                closed_frames
                                >= MIN_CLOSED_FRAMES
                        ):
                            eyes_were_closed = True

                    elif (
                            eyes_were_closed
                            and average_blink
                            <= BLINK_OPEN_THRESHOLD
                    ):

                        blink_completed = True

                        closed_frames = 0
                        eyes_were_closed = False

                        state = "WAIT_TURN"

                        print("Blink detected!")

                        print(
                            "Now turn your head "
                            "LEFT or RIGHT."
                        )

                    elif (
                            average_blink
                            <= BLINK_OPEN_THRESHOLD
                    ):

                        closed_frames = 0

                # =============================================
                # STATE 3 - TURN HEAD
                # =============================================

                elif state == "WAIT_TURN":

                    instruction = (
                        "TURN HEAD LEFT OR RIGHT"
                    )

                    head_delta = abs(
                        head_position
                        - baseline_head_position
                    )

                    if (
                            head_delta
                            >= HEAD_TURN_THRESHOLD
                    ):

                        head_turn_completed = True

                        state = "WAIT_RETURN"

                        print(
                            "Head turn detected!"
                        )

                        print(
                            "Return your face "
                            "to the center."
                        )

                # =============================================
                # STATE 4 - RETURN TO CENTER
                # =============================================

                elif state == "WAIT_RETURN":

                    instruction = (
                        "RETURN FACE TO CENTER"
                    )

                    head_delta = abs(
                        head_position
                        - baseline_head_position
                    )

                    if (
                            head_delta
                            <= RETURN_CENTER_THRESHOLD
                    ):

                        liveness_passed = True
                        state = "PASSED"

                        print()
                        print("=" * 40)
                        print("       LIVENESS PASSED!")
                        print("=" * 40)

                # =============================================
                # PASSED
                # =============================================

                elif state == "PASSED":

                    instruction = (
                        "LIVENESS PASSED"
                    )

                # Calculate debug delta
                if (
                        baseline_head_position
                        is not None
                ):

                    head_delta = abs(
                        head_position
                        - baseline_head_position
                    )

                # =============================================
                # DEBUG VALUES
                # =============================================

                cv2.putText(
                    frame,
                    (
                        f"Blink L: "
                        f"{blink_left:.2f}"
                    ),
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    (
                        f"Blink R: "
                        f"{blink_right:.2f}"
                    ),
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    (
                        f"Head delta: "
                        f"{head_delta:.3f}"
                    ),
                    (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2
                )

            else:

                instruction = "NO FACE DETECTED"

            # =================================================
            # USER INTERFACE
            # =================================================

            if liveness_passed:

                instruction_color = (
                    0,
                    255,
                    0
                )

            else:

                instruction_color = (
                    0,
                    255,
                    255
                )

            cv2.putText(
                frame,
                instruction,
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                instruction_color,
                2
            )

            # Blink status

            blink_status = (
                "Blink: PASS"
                if blink_completed
                else "Blink: WAITING"
            )

            blink_color = (
                (0, 255, 0)
                if blink_completed
                else (255, 255, 255)
            )

            cv2.putText(
                frame,
                blink_status,
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                blink_color,
                2
            )

            # Head turn status

            head_status = (
                "Head Turn: PASS"
                if head_turn_completed
                else "Head Turn: WAITING"
            )

            head_color = (
                (0, 255, 0)
                if head_turn_completed
                else (255, 255, 255)
            )

            cv2.putText(
                frame,
                head_status,
                (20, 230),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                head_color,
                2
            )

            # Overall state

            cv2.putText(
                frame,
                f"State: {state}",
                (20, 270),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "Smart Face Attendance - Liveness",
                frame
            )

            if (
                    cv2.waitKey(1)
                    & 0xFF
                    == ord("q")
            ):
                break

    camera.release()
    cv2.destroyAllWindows()

    print("Liveness test stopped.")


if __name__ == "__main__":
    run_liveness_test()