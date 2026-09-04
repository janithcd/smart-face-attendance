import cv2
import json
from pathlib import Path


MODEL_FILE = Path("data/models/face_model.yml")
LABELS_FILE = Path("data/models/labels.json")

FACE_SIZE = (200, 200)

# With LBPH, LOWER distance means a better match.
# You may adjust this value later.
RECOGNITION_THRESHOLD = 65


def recognize_faces():

    if not MODEL_FILE.exists():
        print("Error: Trained model not found.")
        print("Run: python train_model.py")
        return

    if not LABELS_FILE.exists():
        print("Error: Label file not found.")
        return

    # Load registered person information
    with open(
            LABELS_FILE,
            "r",
            encoding="utf-8"
    ) as file:
        labels = json.load(file)

    # Load trained recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    recognizer.read(
        str(MODEL_FILE)
    )

    # Load face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    if face_cascade.empty():
        print("Error: Could not load face detector.")
        return

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    print("=" * 40)
    print("       FACE RECOGNITION STARTED")
    print("=" * 40)
    print("Press Q to close.")

    while True:

        success, frame = camera.read()

        if not success:
            print("Error: Could not read camera frame.")
            break

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

            face = gray_frame[
                y:y + height,
                x:x + width
            ]

            face = cv2.resize(
                face,
                FACE_SIZE
            )

            label, distance = recognizer.predict(face)

            # Lower LBPH distance means a better match
            if (
                    distance < RECOGNITION_THRESHOLD
                    and str(label) in labels
            ):

                person = labels[str(label)]

                person_name = person["name"]
                person_id = person["id"]

                display_name = person_name
                display_status = f"ID: {person_id} | Match: {distance:.1f}"

                box_color = (0, 255, 0)

            else:

                display_name = "Unknown Person"
                display_status = f"Match: {distance:.1f}"

                box_color = (0, 0, 255)

            # Face rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + width, y + height),
                box_color,
                2
            )

            # Person name
            cv2.putText(
                frame,
                display_name,
                (x, y - 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                box_color,
                2
            )

            # ID / matching distance
            cv2.putText(
                frame,
                display_status,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                box_color,
                2
            )

        cv2.putText(
            frame,
            "Press Q to exit",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Smart Face Attendance - Recognition",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("Face recognition stopped.")


if __name__ == "__main__":
    recognize_faces()