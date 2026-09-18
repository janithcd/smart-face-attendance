import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from attendance_db import (
    initialize_database,
    get_today_attendance,
    get_all_attendance,
)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

FACES_DIR = BASE_DIR / "data" / "faces"
PEOPLE_MANAGER_SCRIPT = (
        BASE_DIR / "people_manager.py"
)
REGISTER_SCRIPT = BASE_DIR / "register_face.py"
BUILD_DATABASE_SCRIPT = BASE_DIR / "build_sface_embeddings.py"
ATTENDANCE_SCRIPT = BASE_DIR / "verify_identity.py"


# =========================================================
# DASHBOARD
# =========================================================

class AttendanceDashboard(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Smart Face Attendance System")

        self.geometry("1100x700")

        self.minsize(
            950,
            600
        )

        initialize_database()

        self.create_styles()
        self.create_header()
        self.create_stats()
        self.create_actions()
        self.create_attendance_table()
        self.create_status_bar()

        self.update_clock()
        self.refresh_dashboard()

    # =====================================================
    # STYLE
    # =====================================================

    def create_styles(self):

        style = ttk.Style(self)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Title.TLabel",
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        )

        style.configure(
            "Subtitle.TLabel",
            font=(
                "Segoe UI",
                10
            )
        )

        style.configure(
            "StatValue.TLabel",
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        )

        style.configure(
            "StatTitle.TLabel",
            font=(
                "Segoe UI",
                10
            )
        )

        style.configure(
            "Action.TButton",
            font=(
                "Segoe UI",
                11
            ),
            padding=10
        )

        style.configure(
            "Treeview",
            rowheight=30,
            font=(
                "Segoe UI",
                10
            )
        )

        style.configure(
            "Treeview.Heading",
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = ttk.Frame(
            self,
            padding=(
                25,
                20
            )
        )

        header.pack(
            fill="x"
        )

        left = ttk.Frame(header)

        left.pack(
            side="left"
        )

        ttk.Label(
            left,
            text="Smart Face Attendance",
            style="Title.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            left,
            text=(
                "SFace Recognition + "
                "MediaPipe Liveness Verification"
            ),
            style="Subtitle.TLabel"
        ).pack(
            anchor="w",
            pady=(
                3,
                0
            )
        )

        self.clock_label = ttk.Label(
            header,
            font=(
                "Segoe UI",
                12
            )
        )

        self.clock_label.pack(
            side="right"
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def create_stats(self):

        stats_frame = ttk.Frame(
            self,
            padding=(
                25,
                5
            )
        )

        stats_frame.pack(
            fill="x"
        )

        # Registered users card

        registered_card = ttk.LabelFrame(
            stats_frame,
            text="Registered People",
            padding=20
        )

        registered_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(
                0,
                10
            )
        )

        self.registered_count = ttk.Label(
            registered_card,
            text="0",
            style="StatValue.TLabel"
        )

        self.registered_count.pack()

        ttk.Label(
            registered_card,
            text="Face profiles"
        ).pack()

        # Today's attendance card

        attendance_card = ttk.LabelFrame(
            stats_frame,
            text="Today's Attendance",
            padding=20
        )

        attendance_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        self.today_count = ttk.Label(
            attendance_card,
            text="0",
            style="StatValue.TLabel"
        )

        self.today_count.pack()

        ttk.Label(
            attendance_card,
            text="Verified attendance"
        ).pack()

        # System status card

        system_card = ttk.LabelFrame(
            stats_frame,
            text="System",
            padding=20
        )

        system_card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(
                10,
                0
            )
        )

        self.system_status = ttk.Label(
            system_card,
            text="READY",
            style="StatValue.TLabel"
        )

        self.system_status.pack()

        ttk.Label(
            system_card,
            text="Recognition system"
        ).pack()

    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    def create_actions(self):

        action_frame = ttk.LabelFrame(
            self,
            text="Actions",
            padding=15
        )

        action_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        register_button = ttk.Button(
            action_frame,
            text="Register Person",
            style="Action.TButton",
            command=self.register_person
        )

        register_button.pack(
            side="left",
            padx=5
        )

        people_button = ttk.Button(
            action_frame,
            text="Manage People",
            style="Action.TButton",
            command=self.manage_people
        )

        people_button.pack(
            side="left",
            padx=5
        )

        build_button = ttk.Button(
            action_frame,
            text="Build Face Database",
            style="Action.TButton",
            command=self.build_face_database
        )

        build_button.pack(
            side="left",
            padx=5
        )

        attendance_button = ttk.Button(
            action_frame,
            text="Start Attendance",
            style="Action.TButton",
            command=self.start_attendance
        )

        attendance_button.pack(
            side="left",
            padx=5
        )

        refresh_button = ttk.Button(
            action_frame,
            text="Refresh",
            style="Action.TButton",
            command=self.refresh_dashboard
        )

        refresh_button.pack(
            side="left",
            padx=5
        )

        export_button = ttk.Button(
            action_frame,
            text="Export CSV",
            style="Action.TButton",
            command=self.export_attendance
        )

        export_button.pack(
            side="left",
            padx=5
        )

        exit_button = ttk.Button(
            action_frame,
            text="Exit",
            style="Action.TButton",
            command=self.destroy
        )

        exit_button.pack(
            side="right",
            padx=5
        )

    # =====================================================
    # ATTENDANCE TABLE
    # =====================================================

    def create_attendance_table(self):

        table_frame = ttk.LabelFrame(
            self,
            text="Today's Attendance",
            padding=15
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(
                0,
                15
            )
        )

        columns = (
            "person_id",
            "name",
            "date",
            "time",
            "verification"
        )

        self.attendance_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.attendance_table.heading(
            "person_id",
            text="ID"
        )

        self.attendance_table.heading(
            "name",
            text="Name"
        )

        self.attendance_table.heading(
            "date",
            text="Date"
        )

        self.attendance_table.heading(
            "time",
            text="Time"
        )

        self.attendance_table.heading(
            "verification",
            text="Verification"
        )

        self.attendance_table.column(
            "person_id",
            width=100,
            anchor="center"
        )

        self.attendance_table.column(
            "name",
            width=260
        )

        self.attendance_table.column(
            "date",
            width=130,
            anchor="center"
        )

        self.attendance_table.column(
            "time",
            width=130,
            anchor="center"
        )

        self.attendance_table.column(
            "verification",
            width=180,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.attendance_table.yview
        )

        self.attendance_table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.attendance_table.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # STATUS BAR
    # =====================================================

    def create_status_bar(self):

        self.status_label = ttk.Label(
            self,
            text="System ready.",
            relief="sunken",
            anchor="w",
            padding=5
        )

        self.status_label.pack(
            side="bottom",
            fill="x"
        )

    # =====================================================
    # CLOCK
    # =====================================================

    def update_clock(self):

        now = datetime.now()

        self.clock_label.config(
            text=now.strftime(
                "%A, %d %B %Y   %H:%M:%S"
            )
        )

        self.after(
            1000,
            self.update_clock
        )

    # =====================================================
    # REGISTERED USER COUNT
    # =====================================================

    def get_registered_people_count(self):

        if not FACES_DIR.exists():
            return 0

        return len(
            [
                folder
                for folder in FACES_DIR.iterdir()
                if folder.is_dir()
            ]
        )

    # =====================================================
    # REFRESH
    # =====================================================

    def refresh_dashboard(self):

        try:

            attendance_records = (
                get_today_attendance()
            )

            registered_people = (
                self.get_registered_people_count()
            )

            self.registered_count.config(
                text=str(
                    registered_people
                )
            )

            self.today_count.config(
                text=str(
                    len(
                        attendance_records
                    )
                )
            )

            # Clear current rows

            for item in (
                    self.attendance_table.get_children()
            ):

                self.attendance_table.delete(
                    item
                )

            # Add attendance records

            for record in attendance_records:

                self.attendance_table.insert(
                    "",
                    "end",
                    values=(
                        record[
                            "person_id"
                        ],
                        record[
                            "person_name"
                        ],
                        record[
                            "attendance_date"
                        ],
                        record[
                            "attendance_time"
                        ],
                        record[
                            "verification_method"
                        ]
                    )
                )

            self.status_label.config(
                text=(
                    "Dashboard refreshed "
                    f"at "
                    f"{datetime.now().strftime('%H:%M:%S')}"
                )
            )

        except Exception as error:

            self.status_label.config(
                text=(
                    f"Refresh error: "
                    f"{error}"
                )
            )

        # Automatically refresh every 5 seconds

        self.after(
            5000,
            self.refresh_dashboard
        )

    # =====================================================
    # LAUNCH PYTHON SCRIPT
    # =====================================================

    def launch_script(
            self,
            script_path,
            description
    ):

        if not script_path.exists():

            messagebox.showerror(
                "File Not Found",
                f"Could not find:\n"
                f"{script_path.name}"
            )

            return

        try:

            subprocess.Popen(
                [
                    sys.executable,
                    str(
                        script_path
                    )
                ],
                cwd=str(
                    BASE_DIR
                )
            )

            self.status_label.config(
                text=description
            )

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # =====================================================
    # ACTIONS
    # =====================================================

    def register_person(self):

        self.launch_script(
            REGISTER_SCRIPT,
            "Person registration started."
        )

    def manage_people(self):

        self.launch_script(
            PEOPLE_MANAGER_SCRIPT,
            "Registered people manager opened."
        )

    def build_face_database(self):

        self.launch_script(
            BUILD_DATABASE_SCRIPT,
            "Building SFace database..."
        )

    def start_attendance(self):

        self.launch_script(
            ATTENDANCE_SCRIPT,
            "Attendance verification started."
        )

    # =====================================================
    # CSV EXPORT
    # =====================================================

    def export_attendance(self):

        try:

            records = (
                get_all_attendance()
            )

            if not records:

                messagebox.showinfo(
                    "Export Attendance",
                    "No attendance records found."
                )

                return

            default_name = (
                    "attendance_"
                    + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
                    + ".csv"
            )

            file_path = (
                filedialog.asksaveasfilename(
                    title=(
                        "Export Attendance"
                    ),
                    defaultextension=".csv",
                    initialfile=default_name,
                    filetypes=[
                        (
                            "CSV Files",
                            "*.csv"
                        )
                    ]
                )
            )

            if not file_path:
                return

            with open(
                    file_path,
                    "w",
                    newline="",
                    encoding="utf-8"
            ) as file:

                writer = csv.writer(
                    file
                )

                writer.writerow([
                    "Person ID",
                    "Name",
                    "Date",
                    "Time",
                    "Verification Method"
                ])

                for record in records:

                    writer.writerow([
                        record[
                            "person_id"
                        ],
                        record[
                            "person_name"
                        ],
                        record[
                            "attendance_date"
                        ],
                        record[
                            "attendance_time"
                        ],
                        record[
                            "verification_method"
                        ]
                    ])

            messagebox.showinfo(
                "Export Complete",
                (
                    "Attendance exported "
                    "successfully."
                )
            )

            self.status_label.config(
                text=(
                    f"Attendance exported: "
                    f"{file_path}"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app = AttendanceDashboard()

    app.mainloop()
