import cv2
import json
import numpy as np
from pathlib import Path


FACES_DIR = Path("data/faces")
MODEL_DIR = Path("data/models")

MODEL_FILE = MODEL_DIR / "face_model.yml"
LABELS_FILE = MODEL_DIR / "labels.json"

FACE_SIZE = (200, 200)


def train_model():
    if not FACES_DIR.exists():
        print("Error: Face dataset folder does not exist.")
        print("Register a person first.")
        return

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    training_faces = []
    training_labels = []

    label_map = {}

    current_label = 0

    person_folders = sorted(
        folder
        for folder in FACES_DIR.iterdir()
        if folder.is_dir()
    )

    if not person_folders:
        print("Error: No registered people found.")
        return

    print("=" * 45)
    print("       TRAINING FACE RECOGNITION MODEL")
    print("=" * 45)

    for person_folder in person_folders:

        folder_name = person_folder.name

        try:
            person_id, safe_name = folder_name.split("_", 1)
        except ValueError:
            print(f"Skipping invalid folder: {folder_name}")
            continue

        person_name = safe_name.replace("_", " ")

        label_map[str(current_label)] = {
            "id": person_id,
            "name": person_name
        }

        image_files = list(person_folder.glob("*.jpg"))

        print()
        print(f"Person: {person_name}")
        print(f"ID: {person_id}")
        print(f"Images: {len(image_files)}")

        for image_path in image_files:

            image = cv2.imread(
                str(image_path),
                cv2.IMREAD_GRAYSCALE
            )

            if image is None:
                print(f"Could not read: {image_path}")
                continue

            image = cv2.resize(
                image,
                FACE_SIZE
            )

            training_faces.append(image)
            training_labels.append(current_label)

        current_label += 1

    if not training_faces:
        print("Error: No valid training images found.")
        return

    labels_array = np.array(
        training_labels,
        dtype=np.int32
    )

    recognizer = cv2.face.LBPHFaceRecognizer_create()

    print()
    print("Training model...")

    recognizer.train(
        training_faces,
        labels_array
    )

    recognizer.write(
        str(MODEL_FILE)
    )

    with open(
            LABELS_FILE,
            "w",
            encoding="utf-8"
    ) as file:
        json.dump(
            label_map,
            file,
            indent=4
        )

    print()
    print("=" * 45)
    print("Training completed successfully!")
    print(f"People trained: {len(label_map)}")
    print(f"Images used: {len(training_faces)}")
    print(f"Model saved: {MODEL_FILE}")
    print("=" * 45)


if __name__ == "__main__":
    train_model()