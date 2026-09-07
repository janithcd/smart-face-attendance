from attendance_db import (
    get_today_attendance
)


def display_today():

    records = get_today_attendance()

    print()
    print("=" * 75)
    print("                     TODAY'S ATTENDANCE")
    print("=" * 75)

    if not records:

        print("No attendance recorded today.")
        return

    print(
        f"{'ID':<10}"
        f"{'Name':<30}"
        f"{'Date':<15}"
        f"{'Time':<12}"
    )

    print("-" * 75)

    for record in records:

        print(
            f"{record['person_id']:<10}"
            f"{record['person_name']:<30}"
            f"{record['attendance_date']:<15}"
            f"{record['attendance_time']:<12}"
        )

    print("-" * 75)

    print(
        f"Total attendance: "
        f"{len(records)}"
    )


if __name__ == "__main__":
    display_today()