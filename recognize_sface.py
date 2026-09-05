import cv2
import numpy as np
from pathlib import Path


YUNET_MODEL = Path(
    "models/face_detection_yunet_2023mar.onnx"
)

SFACE_MODEL = Path(
    "models/face_recognition_sface_2021dec.onnx"
)

DATABASE_FILE = Path(
    "data/models/sface_database.npz"
)


# OpenCV benchmark threshold is 0.363.
# We use a stricter starting threshold for attendance.
MATCH_THRESHOLD = 0.45


def normalize_embedding(embedding):

    embedding = embedding.astype(np.float32)

    norm = np.linalg.norm(embedding)

    if norm == 0:
        return embedding

    return embedding / norm


def recognize():

    if not DATABASE_FILE.exists():
        print("Error: SFace database not found.")
        print("Run: python build_sface_embeddings.py")
        return

    database = np.load(
        DATABASE_FILE,
        allow_pickle=False
    )

    known_embeddings = database[
        "embeddings"
    ].astype(np.float32)

    person_ids = database["ids"]
    person_names = database["names"]

    detector = cv2.FaceDetectorYN.create(
        str(YUNET_MODEL),
        "",
        (320, 320),
        0.8,
        0.3,
        5000
    )

    recognizer = cv2.FaceRecognizerSF.create(
        str(SFACE_MODEL),
        ""
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    print("=" * 45)
    print("       SFACE RECOGNITION STARTED")
    print("=" * 45)
    print("Press Q to exit.")

    while True:

        success, frame = camera.read()

        if not success:
            break

        height, width = frame.shape[:2]

        detector.setInputSize(
            (width, height)
        )

        _, faces = detector.detect(frame)

        if faces is not None:

            for face in faces:

                x = int(face[0])
                y = int(face[1])
                w = int(face[2])
                h = int(face[3])

                aligned_face = recognizer.alignCrop(
                    frame,
                    face
                )

                current_embedding = recognizer.feature(
                    aligned_face
                )

                current_embedding = normalize_embedding(
                    current_embedding
                )

                best_score = -1.0
                best_index = -1

                for index, known_embedding in enumerate(
                        known_embeddings
                ):

                    known_embedding = known_embedding.reshape(
                        1,
                        -1
                    )

                    score = recognizer.match(
                        current_embedding,
                        known_embedding,
                        cv2.FaceRecognizerSF_FR_COSINE
                    )

                    if score > best_score:
                        best_score = score
                        best_index = index

                if (
                        best_index >= 0
                        and best_score >= MATCH_THRESHOLD
                ):

                    name = str(
                        person_names[best_index]
                    )

                    person_id = str(
                        person_ids[best_index]
                    )

                    label = name
                    details = (
                        f"ID: {person_id} | "
                        f"Similarity: {best_score:.3f}"
                    )

                    color = (0, 255, 0)

                else:

                    label = "Unknown Person"
                    details = (
                        f"Similarity: {best_score:.3f}"
                    )

                    color = (0, 0, 255)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x, max(30, y - 35)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    details,
                    (x, max(55, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    color,
                    2
                )

        cv2.putText(
            frame,
            f"Threshold: {MATCH_THRESHOLD:.2f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Smart Face Attendance - SFace",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    print("Recognition stopped.")


if __name__ == "__main__":
    recognize()