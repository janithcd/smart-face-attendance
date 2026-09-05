# Smart Face Attendance

A Python-based smart attendance system that uses **face recognition and liveness verification** to identify registered users and help prevent attendance spoofing using static photos.

The project combines modern computer vision models with real-time webcam processing and is being developed step by step as a practical AI/computer-vision portfolio project.

---

## Project Overview

Traditional attendance systems can be slow, manual, or easy to manipulate.

Smart Face Attendance aims to provide an automated workflow:

```text
Webcam
   ↓
Face Detection
   ↓
Face Recognition
   ↓
Identity Verification
   ↓
Liveness Check
   ↓
Attendance Recording
```

Before attendance is accepted, the system verifies both:

* Who the person is
* Whether a real person is currently in front of the camera

---

## Current Features

* Real-time webcam capture
* Face detection
* Person registration
* Automatic face image dataset collection
* YuNet DNN face detection
* SFace deep face embeddings
* Face recognition using cosine similarity
* Multiple-frame identity confirmation
* Unknown-person rejection
* MediaPipe Face Landmarker integration
* Blink detection
* Head-turn detection
* Return-to-center verification
* Basic static-photo spoof prevention
* Identity lock during liveness verification
* Multiple-person detection protection

---

## Recognition and Liveness Flow

The current verification pipeline works like this:

```text
Camera
   ↓
YuNet Face Detector
   ↓
SFace Recognition
   ↓
Same identity detected
for multiple frames
   ↓
Identity Locked
   ↓
Face Landmarker
   ↓
Look Straight
   ↓
Blink
   ↓
Turn Head
   ↓
Return to Center
   ↓
IDENTITY + LIVENESS VERIFIED
```

A static photograph may still be recognized as the correct person by SFace because the photograph genuinely contains that person's face.

However, the liveness stage should prevent a static image from completing the required actions.

Example:

```text
Photo of Janith
      ↓
Identity: PASS
      ↓
Blink challenge: FAIL
      ↓
Verification rejected
```

---

## Technologies Used

* Python
* OpenCV
* OpenCV Contrib
* NumPy
* YuNet
* SFace
* MediaPipe Tasks
* TensorFlow Lite runtime used internally by MediaPipe

Future versions will also use:

* SQLite
* Attendance database
* Admin interface
* CSV reporting

---

## AI / Computer Vision Models

The project currently uses three model files.

```text
models/
├── face_detection_yunet_2023mar.onnx
├── face_recognition_sface_2021dec.onnx
└── face_landmarker.task
```

### YuNet

Used for real-time face detection and facial landmarks required by the SFace pipeline.

### SFace

Used to generate numerical face embeddings and compare registered users with faces detected through the webcam.

Higher cosine similarity generally means the faces are more similar.

### MediaPipe Face Landmarker

Used for liveness verification, including:

* Eye blink detection
* Facial landmarks
* Head movement detection

---

## Project Structure

```text
smart-face-attendance/
│
├── data/
│   ├── faces/
│   │   └── 001_Janith_Dasanayaka/
│   │       ├── face_001.jpg
│   │       ├── face_002.jpg
│   │       └── ...
│   │
│   └── models/
│       └── sface_database.npz
│
├── models/
│   ├── face_detection_yunet_2023mar.onnx
│   ├── face_recognition_sface_2021dec.onnx
│   └── face_landmarker.task
│
├── main.py
├── register_face.py
├── train_model.py
├── recognize_face.py
├── build_sface_embeddings.py
├── recognize_sface.py
├── test_landmarker.py
├── liveness_test.py
├── verify_identity.py
├── requirements.txt
├── .gitignore
└── README.md
```

Some earlier LBPH files are currently retained because they show how the project evolved from basic recognition to a more advanced deep-learning-based solution.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/janithcd/smart-face-attendance.git
```

Enter the project directory:

```bash
cd smart-face-attendance
```

---

## 2. Create a Python virtual environment

On Windows:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Your terminal should look similar to:

```text
(.venv) PS C:\Users\User\Desktop\smart-face-attendance>
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

The project currently uses packages including:

```text
opencv-contrib-python
numpy
mediapipe
```

---

# Required Model Files

AI model files are intentionally excluded from the Git repository.

Download and place the following files inside the `models` directory.

```text
models/
├── face_detection_yunet_2023mar.onnx
├── face_recognition_sface_2021dec.onnx
└── face_landmarker.task
```

The YuNet and SFace models are available from the official OpenCV Zoo.

The Face Landmarker model is available from Google's MediaPipe model resources.

---

# Usage

## 1. Register a Person

Run:

```bash
python register_face.py
```

Example:

```text
Enter Person ID: 001
Enter Person Name: Janith Dasanayaka
```

The webcam will open and automatically collect multiple face images.

The dataset will be stored locally:

```text
data/faces/001_Janith_Dasanayaka/
```

Example:

```text
face_001.jpg
face_002.jpg
face_003.jpg
...
face_030.jpg
```

Move your head slightly while capturing the dataset to provide some variation.

---

## 2. Build the SFace Database

After registering users, run:

```bash
python build_sface_embeddings.py
```

The application processes registered face images and generates SFace embeddings.

Example output:

```text
Processing: Janith Dasanayaka
Valid images: 28/30

SFace database created successfully!
Registered people: 1
```

The generated database is stored at:

```text
data/models/sface_database.npz
```

---

## 3. Test Face Recognition

Run:

```bash
python recognize_sface.py
```

A recognized person should appear similar to:

```text
Janith Dasanayaka
ID: 001
Similarity: 0.72
```

An unrecognized person should appear as:

```text
Unknown Person
Similarity: 0.24
```

The current recognition threshold can be adjusted depending on camera quality, lighting conditions, and testing results.

---

## 4. Test Liveness Detection

Run:

```bash
python liveness_test.py
```

The liveness sequence is:

```text
LOOK STRAIGHT AT CAMERA
        ↓
BLINK ONCE
        ↓
TURN HEAD LEFT OR RIGHT
        ↓
RETURN FACE TO CENTER
        ↓
LIVENESS PASSED
```

This stage uses MediaPipe facial landmarks and blendshapes.

---

## 5. Run Identity + Liveness Verification

Run:

```bash
python verify_identity.py
```

The full verification pipeline performs:

```text
Face Detection
      ↓
Face Recognition
      ↓
Identity Stable for Multiple Frames
      ↓
Identity Locked
      ↓
Liveness Verification
      ↓
Verification Passed
```

Successful verification produces output similar to:

```text
==================================================
IDENTITY + LIVENESS VERIFIED!
Person: Janith Dasanayaka
ID: 001
==================================================
```

Controls:

```text
Q = Quit
R = Reset Verification
```

---

# Anti-Spoofing Behaviour

One of the major goals of the project is reducing attendance spoofing.

### Real Person

```text
Identity Recognition ✓
Blink ✓
Head Turn ✓
Return to Center ✓

VERIFICATION PASSED
```

### Static Photograph

```text
Identity Recognition may pass
Blink ✗

VERIFICATION FAILED
```

### Unknown Person

```text
Face detected
Identity does not meet similarity threshold

UNKNOWN PERSON
```

This is currently a **basic challenge-response liveness system** and should not be considered equivalent to production-grade biometric security systems used by banks or government identity platforms.

---

# Privacy and Security

Face datasets and generated biometric representations are intentionally excluded from Git.

```

This prevents registered face images and generated biometric embeddings from being uploaded to the public GitHub repository.

---

# Project Development Progress

## Phase 1 — Environment and Camera

* [x] Python environment
* [x] Virtual environment
* [x] OpenCV installation
* [x] Webcam integration

## Phase 2 — Face Detection

* [x] Haar Cascade face detection
* [x] Real-time face bounding boxes

## Phase 3 — Registration

* [x] Person ID input
* [x] Person name input
* [x] Automatic dataset folder creation
* [x] Face image collection

## Phase 4 — Recognition

* [x] Basic LBPH recognition
* [x] Identify limitations of LBPH
* [x] Upgrade to YuNet
* [x] Upgrade to SFace
* [x] Generate deep face embeddings
* [x] Cosine similarity matching
* [x] Unknown-person detection
* [x] Multi-frame identity confirmation

## Phase 5 — Liveness

* [x] MediaPipe Face Landmarker
* [x] Eye blink detection
* [x] Head-turn detection
* [x] Return-to-center detection
* [x] Basic static-photo spoof prevention
* [x] Combine identity and liveness verification

## Phase 6 — Attendance System

* [ ] SQLite database
* [ ] Automatically record attendance
* [ ] Date and time recording
* [ ] Prevent duplicate attendance
* [ ] Attendance history

## Phase 7 — Application Interface

* [ ] Admin dashboard
* [ ] Person management
* [ ] Attendance viewer
* [ ] Search and filtering
* [ ] CSV export
* [ ] Improved user interface

---

# Current Development Status

The computer-vision verification layer is currently functional.

The system can:

```text
Register Person
      ↓
Build Face Embedding
      ↓
Recognize Person
      ↓
Perform Liveness Challenge
      ↓
Verify Identity
```

The next major development stage is:

```text
SQLite Attendance Database
```

Successful identity + liveness verification will automatically record:

```text
Person ID
Name
Date
Time
Attendance Status
```

while preventing duplicate attendance records for the same person on the same day.

---

# Author

**Janith Dasanayaka**

Software Engineering student and aspiring Full-Stack / Software Developer.

---

## Repository

Smart Face Attendance

`janithcd/smart-face-attendance`
