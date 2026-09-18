import shutil
import subprocess
import sys
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox


BASE_DIR = Path(__file__).resolve().parent

FACES_DIR = BASE_DIR / "data" / "faces"
SFACE_DATABASE = BASE_DIR / "data" / "models" / "sface_database.npz"

REGISTER_SCRIPT = BASE_DIR / "register_face.py"
BUILD_DATABASE_SCRIPT = BASE_DIR / "build_sface_embeddings.py"


class PeopleManager(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Registered People - Smart Face Attendance")
        self.geometry("850x550")
        self.minsize(750, 500)

        self.create_ui()
        self.refresh_people()

    def create_ui(self):

        header = ttk.Frame(
            self,
            padding=20
        )
        header.pack(fill="x")

        ttk.Label(
            header,
            text="Registered People",
            font=("Segoe UI", 22, "bold")
        ).pack(
            side="left"
        )

        self.count_label = ttk.Label(
            header,
            text="0 people",
            font=("Segoe UI", 11)
        )
        self.count_label.pack(
            side="right"
        )

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        actions = ttk.Frame(
            self,
            padding=(20, 0, 20, 15)
        )
        actions.pack(fill="x")

        ttk.Button(
            actions,
            text="Register New Person",
            command=self.register_person
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            actions,
            text="Refresh",
            command=self.refresh_people
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            actions,
            text="Rebuild Face Database",
            command=self.rebuild_database
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            actions,
            text="Delete Selected",
            command=self.delete_selected
        ).pack(
            side="right",
            padx=5
        )

        # -------------------------------------------------
        # Table
        # -------------------------------------------------

        table_frame = ttk.Frame(
            self,
            padding=(20, 0, 20, 10)
        )
        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "id",
            "name",
            "images",
            "folder"
        )

        self.people_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.people_table.heading(
            "id",
            text="Person ID"
        )

        self.people_table.heading(
            "name",
            text="Name"
        )

        self.people_table.heading(
            "images",
            text="Face Images"
        )

        self.people_table.heading(
            "folder",
            text="Dataset Folder"
        )

        self.people_table.column(
            "id",
            width=100,
            anchor="center"
        )

        self.people_table.column(
            "name",
            width=220
        )

        self.people_table.column(
            "images",
            width=120,
            anchor="center"
        )

        self.people_table.column(
            "folder",
            width=300
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.people_table.yview
        )

        self.people_table.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.people_table.pack(
            fill="both",
            expand=True
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        self.status_label = ttk.Label(
            self,
            text="Ready.",
            relief="sunken",
            anchor="w",
            padding=6
        )

        self.status_label.pack(
            fill="x",
            side="bottom"
        )

    # =====================================================
    # READ REGISTERED PEOPLE
    # =====================================================

    def get_registered_people(self):

        people = []

        if not FACES_DIR.exists():
            return people

        for folder in sorted(FACES_DIR.iterdir()):

            if not folder.is_dir():
                continue

            folder_name = folder.name

            try:
                person_id, safe_name = folder_name.split(
                    "_",
                    1
                )

            except ValueError:
                continue

            person_name = safe_name.replace(
                "_",
                " "
            )

            image_count = len(
                list(folder.glob("*.jpg"))
            )

            people.append({
                "id": person_id,
                "name": person_name,
                "images": image_count,
                "folder": folder
            })

        return people

    # =====================================================
    # REFRESH TABLE
    # =====================================================

    def refresh_people(self):

        for item in self.people_table.get_children():
            self.people_table.delete(item)

        people = self.get_registered_people()

        for person in people:

            self.people_table.insert(
                "",
                "end",
                values=(
                    person["id"],
                    person["name"],
                    person["images"],
                    person["folder"].name
                )
            )

        self.count_label.config(
            text=f"{len(people)} people"
        )

        self.status_label.config(
            text="Registered people refreshed."
        )

    # =====================================================
    # REGISTER
    # =====================================================

    def register_person(self):

        if not REGISTER_SCRIPT.exists():

            messagebox.showerror(
                "Error",
                "register_face.py was not found."
            )

            return

        try:

            subprocess.Popen(
                [
                    sys.executable,
                    str(REGISTER_SCRIPT)
                ],
                cwd=str(BASE_DIR)
            )

            self.status_label.config(
                text=(
                    "Registration started. "
                    "Complete the face capture window."
                )
            )

            # Refresh after registration may have started.
            self.after(
                3000,
                self.refresh_people
            )

        except Exception as error:

            messagebox.showerror(
                "Registration Error",
                str(error)
            )

    # =====================================================
    # REBUILD SFACE DATABASE
    # =====================================================

    def rebuild_database(self):

        if not BUILD_DATABASE_SCRIPT.exists():

            messagebox.showerror(
                "Error",
                "build_sface_embeddings.py was not found."
            )

            return

        try:

            subprocess.Popen(
                [
                    sys.executable,
                    str(BUILD_DATABASE_SCRIPT)
                ],
                cwd=str(BASE_DIR)
            )

            self.status_label.config(
                text="Rebuilding SFace database..."
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    # =====================================================
    # DELETE PERSON
    # =====================================================

    def delete_selected(self):

        selected = self.people_table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Select a person first."
            )

            return

        item = self.people_table.item(
            selected[0]
        )

        values = item["values"]

        person_id = str(values[0])
        person_name = str(values[1])
        folder_name = str(values[3])

        confirm = messagebox.askyesno(
            "Delete Registered Person",
            (
                f"Delete {person_name}?\n\n"
                f"Person ID: {person_id}\n\n"
                "Their local face dataset will be "
                "permanently deleted."
            )
        )

        if not confirm:
            return

        folder_path = FACES_DIR / folder_name

        try:

            if folder_path.exists():
                shutil.rmtree(folder_path)

            # Remove old SFace DB so deleted users cannot
            # remain recognized from stale embeddings.
            if SFACE_DATABASE.exists():
                SFACE_DATABASE.unlink()

            self.refresh_people()

            remaining_people = (
                self.get_registered_people()
            )

            if remaining_people:

                subprocess.Popen(
                    [
                        sys.executable,
                        str(BUILD_DATABASE_SCRIPT)
                    ],
                    cwd=str(BASE_DIR)
                )

                self.status_label.config(
                    text=(
                        f"{person_name} deleted. "
                        "Rebuilding face database..."
                    )
                )

            else:

                self.status_label.config(
                    text=(
                        f"{person_name} deleted. "
                        "No registered people remain."
                    )
                )

            messagebox.showinfo(
                "Person Deleted",
                (
                    f"{person_name} was deleted "
                    "successfully."
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Delete Error",
                str(error)
            )


if __name__ == "__main__":

    app = PeopleManager()
    app.mainloop()