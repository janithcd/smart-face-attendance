import cv2
import mediapipe as mp
import numpy as np
import time
from pathlib import Path


# =========================================================
# FILES
# =========================================================

YUNET_MODEL = Path(
    "models/face_detection_yunet_2023mar.onnx"
)

SFACE_MODEL = Path(
    "models/face_recognition_sface_2021dec.onnx"
)

LANDMARKER_MODEL = Path(
    "models/face_landmarker.task"
)

DATABASE_FILE = Path(
    "data/models/sface_database.npz"
)


# =========================================================
# RECOGNITION SETTINGS
# =========================================================

MATCH_THRESHOLD = 0.45

# Require the same identity several frames in a row
IDENTITY_STABLE_FRAMES = 5

# If the recognized person changes/disappears for several
# frames during liveness, reset authentication.
MAX_IDENTITY_MISMATCH_FRAMES = 5


# =========================================================
# LIVENESS SETTINGS
# =========================================================

BLINK_CLOSED_THRESHOLD = 0.55
BLINK_OPEN_THRESHOLD = 0.25

MIN_CLOSED_FRAMES = 2

HEAD_TURN_THRESHOLD = 0.07
RETURN_CENTER_THRESHOLD = 0.035

BASELINE_FRAMES = 30


# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def normalize_embedding(embedding):

    embedding = embedding.astype(np.float32)

    norm = np.linalg.norm(embedding)

    if norm == 0:
        return embedding

    return embedding / norm


def calculate_head_position(landmarks):

    left_side = landmarks[234].x
    right_side = landmarks[454].x
    nose = landmarks[1].x

    face_width = right_side - left_side

    if abs(face_width) < 0.0001:
        return 0.5

    return (
            nose - left_side
    ) / face_width


def get_blendshape_score(
        blendshapes,
        category_name
):

    for category in blendshapes:

        if (
                category.category_name
                == category_name
        ):
            return category.score

    return 0.0


# =========================================================
# MAIN
# =========================================================

def verify_identity():

    required_files = [
        YUNET_MODEL,
        SFACE_MODEL,
        LANDMARKER_MODEL,
        DATABASE_FILE
    ]

    for file_path in required_files:

        if not file_path.exists():
            print(
                f"Error: Required file "
                f"not found: {file_path}"
            )
            return

    # -----------------------------------------------------
    # LOAD SFACE DATABASE
    # -----------------------------------------------------

    database = np.load(
        DATABASE_FILE,
        allow_pickle=False
    )

    known_embeddings = database[
        "embeddings"
    ].astype(np.float32)

    person_ids = database["ids"]
    person_names = database["names"]

    # -----------------------------------------------------
    # YUNET
    # -----------------------------------------------------

    detector = cv2.FaceDetectorYN.create(
        str(YUNET_MODEL),
        "",
        (320, 320),
        0.8,
        0.3,
        5000
    )

    # -----------------------------------------------------
    # SFACE
    # -----------------------------------------------------

    recognizer = cv2.FaceRecognizerSF.create(
        str(SFACE_MODEL),
        ""
    )

    # -----------------------------------------------------
    # MEDIAPIPE
    # -----------------------------------------------------

    BaseOptions = mp.tasks.BaseOptions

    FaceLandmarker = (
        mp.tasks.vision.FaceLandmarker
    )

    FaceLandmarkerOptions = (
        mp.tasks.vision.FaceLandmarkerOptions
    )

    RunningMode = (
        mp.tasks.vision.RunningMode
    )

    options = FaceLandmarkerOptions(

        base_options=BaseOptions(
            model_asset_path=str(
                LANDMARKER_MODEL
            )
        ),

        running_mode=RunningMode.VIDEO,

        num_faces=1,

        min_face_detection_confidence=0.6,

        min_face_presence_confidence=0.6,

        min_tracking_confidence=0.6,

        output_face_blendshapes=True
    )

    # -----------------------------------------------------
    # CAMERA
    # -----------------------------------------------------

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print(
            "Error: Could not open webcam."
        )
        return

    # -----------------------------------------------------
    # AUTHENTICATION STATE
    # -----------------------------------------------------

    state = "IDENTIFY"

    candidate_index = None
    candidate_frames = 0

    locked_index = None
    identity_mismatch_frames = 0

    baseline_samples = []
    baseline_head_position = None

    closed_frames = 0
    eyes_were_closed = False

    blink_completed = False
    head_turn_completed = False

    verification_passed = False

    last_timestamp = 0

    print("=" * 55)
    print("       SMART FACE ATTENDANCE VERIFICATION")
    print("=" * 55)
    print()
    print("Look at the camera.")
    print("Press Q to quit.")
    print("Press R to reset verification.")
    print()

    # -----------------------------------------------------
    # RESET FUNCTION
    # -----------------------------------------------------

    def reset_verification():

        nonlocal state

        nonlocal candidate_index
        nonlocal candidate_frames

        nonlocal locked_index
        nonlocal identity_mismatch_frames

        nonlocal baseline_samples
        nonlocal baseline_head_position

        nonlocal closed_frames
        nonlocal eyes_were_closed

        nonlocal blink_completed
        nonlocal head_turn_completed

        nonlocal verification_passed

        state = "IDENTIFY"

        candidate_index = None
        candidate_frames = 0

        locked_index = None
        identity_mismatch_frames = 0

        baseline_samples = []
        baseline_head_position = None

        closed_frames = 0
        eyes_were_closed = False

        blink_completed = False
        head_turn_completed = False

        verification_passed = False

        print()
        print("Verification reset.")
        print("Look at the camera.")

    # -----------------------------------------------------
    # START LANDMARKER
    # -----------------------------------------------------

    with FaceLandmarker.create_from_options(
            options
    ) as landmarker:

        while True:

            success, frame = camera.read()

            if not success:
                break

            # Mirror camera
            frame = cv2.flip(frame, 1)

            height, width = frame.shape[:2]

            detector.setInputSize(
                (width, height)
            )

            _, detected_faces = (
                detector.detect(frame)
            )

            current_index = -1
            current_score = -1.0

            display_name = "Unknown"
            display_id = ""

            face_color = (
                0,
                0,
                255
            )

            # =================================================
            # SFACE RECOGNITION
            # =================================================

            if (
                    detected_faces is not None
                    and len(detected_faces) == 1
            ):

                face = detected_faces[0]

                x = int(face[0])
                y = int(face[1])
                w = int(face[2])
                h = int(face[3])

                aligned_face = (
                    recognizer.alignCrop(
                        frame,
                        face
                    )
                )

                current_embedding = (
                    recognizer.feature(
                        aligned_face
                    )
                )

                current_embedding = (
                    normalize_embedding(
                        current_embedding
                    )
                )

                best_score = -1.0
                best_index = -1

                for index, known_embedding in enumerate(
                        known_embeddings
                ):

                    known_embedding = (
                        known_embedding.reshape(
                            1,
                            -1
                        )
                    )

                    score = recognizer.match(
                        current_embedding,
                        known_embedding,
                        cv2.FaceRecognizerSF_FR_COSINE
                    )

                    if score > best_score:

                        best_score = score
                        best_index = index

                current_score = best_score

                if (
                        best_index >= 0
                        and best_score
                        >= MATCH_THRESHOLD
                ):

                    current_index = best_index

                    display_name = str(
                        person_names[
                            best_index
                        ]
                    )

                    display_id = str(
                        person_ids[
                            best_index
                        ]
                    )

                    face_color = (
                        0,
                        255,
                        0
                    )

                # Draw face box

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    face_color,
                    2
                )

                cv2.putText(
                    frame,
                    display_name,
                    (
                        x,
                        max(
                            30,
                            y - 35
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    face_color,
                    2
                )

                cv2.putText(
                    frame,
                    (
                        f"Similarity: "
                        f"{current_score:.3f}"
                    ),
                    (
                        x,
                        max(
                            55,
                            y - 10
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    face_color,
                    2
                )

            elif (
                    detected_faces is not None
                    and len(detected_faces) > 1
            ):

                cv2.putText(
                    frame,
                    "ONLY ONE PERSON ALLOWED",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # =================================================
            # IDENTITY STABILITY CHECK
            # =================================================

            if state == "IDENTIFY":

                instruction = (
                    "LOOK AT CAMERA"
                )

                if current_index >= 0:

                    if (
                            candidate_index
                            == current_index
                    ):

                        candidate_frames += 1

                    else:

                        candidate_index = (
                            current_index
                        )

                        candidate_frames = 1

                    instruction = (
                        f"IDENTIFYING "
                        f"{candidate_frames}/"
                        f"{IDENTITY_STABLE_FRAMES}"
                    )

                    if (
                            candidate_frames
                            >= IDENTITY_STABLE_FRAMES
                    ):

                        locked_index = (
                            candidate_index
                        )

                        state = "CALIBRATING"

                        baseline_samples = []

                        print()
                        print(
                            "Identity recognized:"
                        )

                        print(
                            person_names[
                                locked_index
                            ]
                        )

                        print(
                            "Starting liveness "
                            "verification..."
                        )

                else:

                    candidate_index = None
                    candidate_frames = 0

            # =================================================
            # VERIFY LOCKED IDENTITY HAS NOT CHANGED
            # =================================================

            elif state != "PASSED":

                if (
                        current_index
                        == locked_index
                ):

                    identity_mismatch_frames = 0

                else:

                    identity_mismatch_frames += 1

                    if (
                            identity_mismatch_frames
                            > MAX_IDENTITY_MISMATCH_FRAMES
                    ):

                        print(
                            "Identity lost or changed."
                        )

                        reset_verification()

                        continue

            # =================================================
            # MEDIAPIPE LANDMARKER
            # =================================================

            if (
                    locked_index is not None
                    and state != "IDENTIFY"
            ):

                rgb_frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                mp_image = mp.Image(
                    image_format=(
                        mp.ImageFormat.SRGB
                    ),
                    data=rgb_frame
                )

                timestamp_ms = int(
                    time.perf_counter()
                    * 1000
                )

                if (
                        timestamp_ms
                        <= last_timestamp
                ):

                    timestamp_ms = (
                            last_timestamp + 1
                    )

                last_timestamp = (
                    timestamp_ms
                )

                result = (
                    landmarker.detect_for_video(
                        mp_image,
                        timestamp_ms
                    )
                )

                if (
                        result.face_landmarks
                        and result.face_blendshapes
                ):

                    landmarks = (
                        result.face_landmarks[0]
                    )

                    blendshapes = (
                        result.face_blendshapes[0]
                    )

                    blink_left = (
                        get_blendshape_score(
                            blendshapes,
                            "eyeBlinkLeft"
                        )
                    )

                    blink_right = (
                        get_blendshape_score(
                            blendshapes,
                            "eyeBlinkRight"
                        )
                    )

                    average_blink = (
                                            blink_left
                                            + blink_right
                                    ) / 2.0

                    head_position = (
                        calculate_head_position(
                            landmarks
                        )
                    )

                    # =========================================
                    # CALIBRATION
                    # =========================================

                    if state == "CALIBRATING":

                        instruction = (
                            "LOOK STRAIGHT"
                        )

                        baseline_samples.append(
                            head_position
                        )

                        if (
                                len(
                                    baseline_samples
                                )
                                >= BASELINE_FRAMES
                        ):

                            baseline_head_position = (
                                    sum(
                                        baseline_samples
                                    )
                                    / len(
                                baseline_samples
                            )
                            )

                            state = (
                                "WAIT_BLINK"
                            )

                            print(
                                "Calibration complete."
                            )

                            print(
                                "Please blink once."
                            )

                    # =========================================
                    # BLINK
                    # =========================================

                    elif state == "WAIT_BLINK":

                        instruction = (
                            "BLINK ONCE"
                        )

                        if (
                                average_blink
                                >= BLINK_CLOSED_THRESHOLD
                        ):

                            closed_frames += 1

                            if (
                                    closed_frames
                                    >= MIN_CLOSED_FRAMES
                            ):

                                eyes_were_closed = (
                                    True
                                )

                        elif (
                                eyes_were_closed
                                and average_blink
                                <= BLINK_OPEN_THRESHOLD
                        ):

                            blink_completed = (
                                True
                            )

                            closed_frames = 0

                            eyes_were_closed = (
                                False
                            )

                            state = "WAIT_TURN"

                            print(
                                "Blink detected!"
                            )

                            print(
                                "Turn your head."
                            )

                        elif (
                                average_blink
                                <= BLINK_OPEN_THRESHOLD
                        ):

                            closed_frames = 0

                    # =========================================
                    # HEAD TURN
                    # =========================================

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

                            head_turn_completed = (
                                True
                            )

                            state = (
                                "WAIT_RETURN"
                            )

                            print(
                                "Head turn detected!"
                            )

                            print(
                                "Return to center."
                            )

                    # =========================================
                    # RETURN
                    # =========================================

                    elif state == "WAIT_RETURN":

                        instruction = (
                            "RETURN TO CENTER"
                        )

                        head_delta = abs(
                            head_position
                            - baseline_head_position
                        )

                        if (
                                head_delta
                                <= RETURN_CENTER_THRESHOLD
                        ):

                            state = "PASSED"

                            verification_passed = (
                                True
                            )

                            print()
                            print(
                                "=" * 50
                            )

                            print(
                                "IDENTITY + "
                                "LIVENESS VERIFIED!"
                            )

                            print(
                                f"Person: "
                                f"{person_names[locked_index]}"
                            )

                            print(
                                f"ID: "
                                f"{person_ids[locked_index]}"
                            )

                            print(
                                "=" * 50
                            )

            # =================================================
            # PASSED
            # =================================================

            if state == "PASSED":

                instruction = (
                    "VERIFICATION PASSED"
                )

                cv2.putText(
                    frame,
                    "IDENTITY VERIFIED",
                    (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    "LIVENESS VERIFIED",
                    (20, 145),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            # =================================================
            # STATUS UI
            # =================================================

            if verification_passed:

                status_color = (
                    0,
                    255,
                    0
                )

            else:

                status_color = (
                    0,
                    255,
                    255
                )

            cv2.putText(
                frame,
                instruction,
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                status_color,
                2
            )

            if locked_index is not None:

                cv2.putText(
                    frame,
                    (
                        "Locked Identity: "
                        f"{person_names[locked_index]}"
                    ),
                    (20, 190),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

            cv2.putText(
                frame,
                f"State: {state}",
                (20, 225),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Q = Quit | R = Reset",
                (20, 260),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            cv2.imshow(
                "Smart Face Attendance - Verification",
                frame
            )

            key = (
                    cv2.waitKey(1)
                    & 0xFF
            )

            if key == ord("q"):
                break

            if key == ord("r"):
                reset_verification()

    camera.release()
    cv2.destroyAllWindows()

    print("Verification stopped.")


if __name__ == "__main__":
    verify_identity()