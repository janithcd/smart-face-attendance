import cv2
from pathlib import Path
import re


TOTAL_IMAGES = 30
SAVE_EVERY_N_FRAMES = 5


def clean_name(name):
    """
    Convert a person's name into a safe folder name.
    Example:
    Janith Dasanayaka -> Janith_Dasanayaka
    """
    name = name.strip()
    name = re.sub(r"[^a-zA-Z0-9_-]", "_", name)
    name = re.sub(r"_+", "_", name)

    return name.strip("_")


def register_person():
    print("=" * 40)
    print("     SMART FACE ATTENDANCE")
    print("        PERSON REGISTRATION")
    print("=" * 40)

    person_id = input("Enter Person ID: ").strip()
    person_name = input("Enter Person Name: ").strip()

    if not person_id or not person_name:
        print("Error: Person ID and name are required.")
        return

    safe_name = clean_name(person_name)

    person_folder = Path("data") / "faces" / f"{person_id}_{safe_name}"
    person_folder.mkdir(parents=True, exist_ok=True)

    print()
    print(f"Registering: {person_name}")
    print(f"Person ID: {person_id}")
    print(f"Images will be saved to: {person_folder}")
    print()

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    if face_cascade.empty():
        print("Error: Could not load face detector.")
        return

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    image_count = 0
    frame_count = 0

    print("Camera started.")
    print("Look directly at the camera.")
    print("Move your head slightly while images are captured.")
    print("Press Q to cancel.")
    print()

    while image_count < TOTAL_IMAGES:
        success, frame = camera.read()

        if not success:
            print("Error: Could not read camera frame.")
            break

        frame_count += 1

        gray_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100)
        )

        for (x, y, width, height) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                (0, 255, 0),
                2
            )

            # Save one image every few frames
            if frame_count % SAVE_EVERY_N_FRAMES == 0:

                face_image = frame[
                    y:y + height,
                    x:x + width
                ]

                image_count += 1

                image_path = (
                        person_folder /
                        f"face_{image_count:03d}.jpg"
                )

                cv2.imwrite(
                    str(image_path),
                    face_image
                )

                print(
                    f"Captured: "
                    f"{image_count}/{TOTAL_IMAGES}"
                )

            break

        cv2.putText(
            frame,
            f"Images: {image_count}/{TOTAL_IMAGES}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            person_name,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Press Q to cancel",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Smart Face Attendance - Registration",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Registration cancelled.")
            break

    camera.release()
    cv2.destroyAllWindows()

    if image_count == TOTAL_IMAGES:
        print()
        print("=" * 40)
        print("Registration completed successfully!")
        print(f"Person: {person_name}")
        print(f"ID: {person_id}")
        print(f"Images captured: {image_count}")
        print("=" * 40)


if __name__ == "__main__":
    register_person()