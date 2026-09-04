# Smart Face Attendance

A Python-based face recognition attendance system built using OpenCV.

The goal of this project is to create a smart attendance system that can register users, recognize faces through a webcam, and automatically record attendance.

## Current Features

* Webcam capture using OpenCV
* Real-time face detection
* Face bounding box
* Live camera preview
* Virtual environment setup
* Dependency management using `requirements.txt`

## Planned Features

* Register new users
* Capture face datasets
* Face recognition
* Attendance recording
* SQLite/MySQL database integration
* Attendance history
* Admin dashboard
* CSV report export
* Duplicate attendance prevention

## Technologies

* Python
* OpenCV
* NumPy

More technologies will be added as the project develops.

## Installation

Clone the repository:

```bash
git clone https://github.com/janithcd/smart-face-attendance.git
```

Enter the project directory:

```bash
cd smart-face-attendance
```

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python main.py
```

The webcam window will open and detect faces in real time.

Press:

```text
Q
```

to close the camera.

## Project Status

Currently under development.

### Completed

* [x] Python project setup
* [x] OpenCV setup
* [x] Webcam integration
* [x] Real-time face detection

### Next

* [ ] Person registration
* [ ] Face dataset collection
* [ ] Face recognition
* [ ] Attendance database
* [ ] Admin interface
* [ ] Attendance reports

## Author

Janith Dasanayaka
