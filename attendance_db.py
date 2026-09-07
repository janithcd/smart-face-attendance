import sqlite3
from datetime import datetime
from pathlib import Path


DATABASE_PATH = Path("data/attendance.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the attendance table if it does not exist.
    """

    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS attendance (
                                                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                      person_id TEXT NOT NULL,
                                                      person_name TEXT NOT NULL,
                                                      attendance_date TEXT NOT NULL,
                                                      attendance_time TEXT NOT NULL,
                                                      verification_method TEXT NOT NULL,
                                                      created_at TEXT NOT NULL,

                                                      UNIQUE(
                                                      person_id,
                                                      attendance_date
            )
                )
            """
        )

        connection.commit()


def record_attendance(
        person_id,
        person_name
):
    """
    Record attendance once per person per day.

    Returns:
        (True, time)
            if new attendance was recorded.

        (False, existing_time)
            if attendance already exists today.
    """

    initialize_database()

    now = datetime.now()

    attendance_date = now.strftime(
        "%Y-%m-%d"
    )

    attendance_time = now.strftime(
        "%H:%M:%S"
    )

    created_at = now.isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:

        try:

            connection.execute(
                """
                INSERT INTO attendance (
                    person_id,
                    person_name,
                    attendance_date,
                    attendance_time,
                    verification_method,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    person_id,
                    person_name,
                    attendance_date,
                    attendance_time,
                    "SFace + Liveness",
                    created_at
                )
            )

            connection.commit()

            return True, attendance_time

        except sqlite3.IntegrityError:

            existing_record = connection.execute(
                """
                SELECT attendance_time
                FROM attendance
                WHERE person_id = ?
                  AND attendance_date = ?
                """,
                (
                    person_id,
                    attendance_date
                )
            ).fetchone()

            if existing_record:

                return (
                    False,
                    existing_record[
                        "attendance_time"
                    ]
                )

            return False, None


def get_today_attendance():

    initialize_database()

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    with get_connection() as connection:

        records = connection.execute(
            """
            SELECT *
            FROM attendance
            WHERE attendance_date = ?
            ORDER BY attendance_time ASC
            """,
            (today,)
        ).fetchall()

    return records


if __name__ == "__main__":

    initialize_database()

    print(
        f"Database ready: "
        f"{DATABASE_PATH}"
    )