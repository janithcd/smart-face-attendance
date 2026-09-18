from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# =========================================================
# PROJECT ROOT
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


from attendance_db import (
    initialize_database,
    get_today_attendance,
    get_all_attendance,
)


FACES_DIR = BASE_DIR / "data" / "faces"


# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="Smart Face Attendance API",
    version="1.0.0",
    description=(
        "Backend API for the Smart Face Attendance System."
    ),
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# STARTUP
# =========================================================

initialize_database()


# =========================================================
# HELPERS
# =========================================================

def get_registered_people():

    people = []

    if not FACES_DIR.exists():
        return people

    for folder in sorted(FACES_DIR.iterdir()):

        if not folder.is_dir():
            continue

        try:
            person_id, safe_name = folder.name.split(
                "_",
                1,
            )
        except ValueError:
            continue

        person_name = safe_name.replace(
            "_",
            " ",
        )

        image_count = len(
            list(folder.glob("*.jpg"))
        )

        people.append(
            {
                "id": person_id,
                "name": person_name,
                "face_images": image_count,
            }
        )

    return people


def serialize_attendance(records):

    return [
        {
            "id": record["id"],
            "person_id": record["person_id"],
            "person_name": record["person_name"],
            "date": record["attendance_date"],
            "time": record["attendance_time"],
            "verification_method": record[
                "verification_method"
            ],
        }
        for record in records
    ]


# =========================================================
# ROUTES
# =========================================================

@app.get("/")
def root():

    return {
        "application": "Smart Face Attendance",
        "status": "running",
    }


@app.get("/api/health")
def health():

    return {
        "status": "ok",
    }


@app.get("/api/dashboard")
def dashboard():

    people = get_registered_people()
    today = get_today_attendance()

    return {
        "registered_people": len(people),
        "today_attendance": len(today),
        "system_status": "READY",
        "attendance": serialize_attendance(today),
    }


@app.get("/api/people")
def people():

    return get_registered_people()


@app.get("/api/attendance/today")
def today_attendance():

    return serialize_attendance(
        get_today_attendance()
    )


@app.get("/api/attendance")
def attendance_history():

    return serialize_attendance(
        get_all_attendance()
    )