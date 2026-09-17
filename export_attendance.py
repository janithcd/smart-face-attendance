import csv
from pathlib import Path
from datetime import datetime

from attendance_db import get_all_attendance


EXPORT_DIR = Path("exports")


def export_attendance():

    records = get_all_attendance()

    if not records:
        print("No attendance records found.")
        return

    EXPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    file_path = (
            EXPORT_DIR
            / f"attendance_{timestamp}.csv"
    )

    with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Person ID",
            "Name",
            "Date",
            "Time",
            "Verification Method"
        ])

        for record in records:

            writer.writerow([
                record["person_id"],
                record["person_name"],
                record["attendance_date"],
                record["attendance_time"],
                record["verification_method"]
            ])

    print(
        f"Attendance exported successfully: "
        f"{file_path}"
    )


if __name__ == "__main__":
    export_attendance()