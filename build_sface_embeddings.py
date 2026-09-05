import cv2
import numpy as np
from pathlib import Path


FACES_DIR = Path("data/faces")
MODEL_DIR = Path("models")
DATA_MODEL_DIR = Path("data/models")

YUNET_MODEL = MODEL_DIR / "face_detection_yunet_2023mar.onnx"
SFACE_MODEL = MODEL_DIR / "face_recognition_sface_2021dec.onnx"

DATABASE_FILE = DATA_MODEL_DIR / "sface_database.npz"


def normalize_embedding(embedding):
    embedding = embedding.astype(np.float32)

    norm = np.linalg.norm(embedding)

    if norm == 0:
        return embedding

    return embedding / norm


def build_embeddings():

    print("=" * 50)
    print("       BUILDING SFACE FACE DATABASE")
    print("=" * 50)

    if not YUNET_MODEL.exists():
        print(f"Error: YuNet model not found: {YUNET_MODEL}")
        return

    if not SFACE_MODEL.exists():
        print(f"Error: SFace model not found: {SFACE_MODEL}")
        return

    if not FACES_DIR.exists():
        print("Error: No registered face dataset found.")
        return

    DATA_MODEL_DIR.mkdir(parents=True, exist_ok=True)

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

    all_embeddings = []
    person_ids = []
    person_names = []

    person_folders = sorted(
        folder
        for folder in FACES_DIR.iterdir()
        if folder.is_dir()
    )

    for person_folder in person_folders:

        folder_name = person_folder.name

        try:
            person_id, safe_name = folder_name.split("_", 1)
        except ValueError:
            print(f"Skipping invalid folder: {folder_name}")
            continue

        person_name = safe_name.replace("_", " ")

        print()
        print(f"Processing: {person_name}")

        person_embeddings = []

        image_files = sorted(person_folder.glob("*.jpg"))

        for image_path in image_files:

            image = cv2.imread(str(image_path))

            if image is None:
                continue

            height, width = image.shape[:2]

            detector.setInputSize((width, height))

            _, faces = detector.detect(image)

            if faces is None or len(faces) == 0:
                print(f"No face detected: {image_path.name}")
                continue

            # Select the largest detected face
            face = max(
                faces,
                key=lambda detected_face:
                detected_face[2] * detected_face[3]
            )

            aligned_face = recognizer.alignCrop(
                image,
                face
            )

            embedding = recognizer.feature(
                aligned_face
            )

            embedding = normalize_embedding(
                embedding
            )

            person_embeddings.append(
                embedding.reshape(-1)
            )

        if not person_embeddings:
            print(
                f"WARNING: No valid embeddings for {person_name}"
            )
            continue

        person_embeddings = np.vstack(
            person_embeddings
        )

        # Create one average representation of this person
        average_embedding = np.mean(
            person_embeddings,
            axis=0
        )

        average_embedding = normalize_embedding(
            average_embedding
        ).reshape(-1)

        all_embeddings.append(
            average_embedding
        )

        person_ids.append(person_id)
        person_names.append(person_name)

        print(
            f"Valid images: "
            f"{len(person_embeddings)}/{len(image_files)}"
        )

    if not all_embeddings:
        print("Error: Could not create any face embeddings.")
        return

    np.savez_compressed(
        DATABASE_FILE,
        embeddings=np.vstack(all_embeddings),
        ids=np.array(person_ids),
        names=np.array(person_names)
    )

    print()
    print("=" * 50)
    print("SFace database created successfully!")
    print(f"Registered people: {len(person_names)}")
    print(f"Saved to: {DATABASE_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    build_embeddings()