
import tkinter as tk
from tkinter import ttk, messagebox
import re

import database as db


class StudentManagementSystem:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1100x700")
        self.root.minsize(850, 600)
        self.root.configure(bg="#eaf2f8")

        self.user_id = None
        self.fullname = ""
        self.selected_id = None

        self.show_login()

    # ---------------- COMMON ----------------

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def heading(self, title):
        tk.Label(
            self.root,
            text=title,
            bg="#154360",
            fg="white",
            font=("Arial", 21, "bold"),
            pady=18
        ).pack(fill="x")

    def button(self, parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold"),
            width=24,
            pady=8,
            cursor="hand2"
        )

    # ---------------- LOGIN PAGE ----------------

    def show_login(self, username=""):
        self.clear_screen()
        self.heading("STUDENT MANAGEMENT SYSTEM")

        frame = tk.Frame(
            self.root, bg="white", padx=45, pady=30
        )
        frame.pack(pady=65)

        tk.Label(
            frame,
            text="ADMIN LOGIN",
            font=("Arial", 21, "bold"),
            fg="#154360",
            bg="white"
        ).pack(pady=15)

        tk.Label(frame, text="Username", bg="white").pack(anchor="w")

        self.username_entry = tk.Entry(
            frame, width=32, font=("Arial", 12)
        )
        self.username_entry.pack(pady=8)
        self.username_entry.insert(0, username)

        tk.Label(frame, text="Password", bg="white").pack(anchor="w")

        self.password_entry = tk.Entry(
            frame, width=32, font=("Arial", 12), show="*"
        )
        self.password_entry.pack(pady=8)

        self.button(
            frame, "LOGIN", self.login, "#154360"
        ).pack(pady=12)

        self.button(
            frame, "CREATE NEW ACCOUNT",
            self.show_register, "#229954"
        ).pack(pady=5)

        self.password_entry.bind(
            "<Return>", lambda event: self.login()
        )

    # ---------------- LOGIN FUNCTION ----------------

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror(
                "Error", "Enter username and password."
            )
            return

        try:
            user = db.login_user(username, password)

            if user:
                self.user_id, self.fullname = user
                self.show_dashboard()
            else:
                messagebox.showerror(
                    "Login Failed", "Invalid username or password."
                )

        except Exception as error:
            messagebox.showerror("Login Error", str(error))

    # ---------------- REGISTER PAGE ----------------

    def show_register(self):
        self.clear_screen()
        self.heading("USER REGISTRATION")

        frame = tk.Frame(
            self.root, bg="white", padx=45, pady=20
        )
        frame.pack(pady=25)

        tk.Label(
            frame,
            text="CREATE ACCOUNT",
            font=("Arial", 19, "bold"),
            fg="#154360",
            bg="white"
        ).pack(pady=10)

        self.reg_entries = {}

        fields = [
            "Full Name", "Username", "Email",
            "Password", "Confirm Password"
        ]

        for field in fields:
            tk.Label(
                frame,
                text=field,
                bg="white",
                font=("Arial", 10, "bold")
            ).pack(anchor="w")

            entry = tk.Entry(
                frame,
                width=35,
                font=("Arial", 11),
                show="*" if "Password" in field else ""
            )
            entry.pack(pady=5)

            self.reg_entries[field] = entry

        self.button(
            frame, "REGISTER", self.register, "#154360"
        ).pack(pady=10)

        self.button(
            frame, "BACK TO LOGIN", self.show_login, "#c0392b"
        ).pack()

    # ---------------- REGISTER FUNCTION ----------------

    def register(self):
        fullname = self.reg_entries["Full Name"].get().strip()
        username = self.reg_entries["Username"].get().strip()
        email = self.reg_entries["Email"].get().strip()
        password = self.reg_entries["Password"].get()
        confirm = self.reg_entries["Confirm Password"].get()

        if not all([fullname, username, email, password, confirm]):
            messagebox.showerror(
                "Error", "Please fill all fields."
            )
            return

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            messagebox.showerror(
                "Error", "Enter a valid email."
            )
            return

        if len(username) < 3:
            messagebox.showerror(
                "Error", "Username must be at least 3 characters."
            )
            return

        if len(password) < 8:
            messagebox.showerror(
                "Error", "Password must be at least 8 characters."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Error", "Passwords do not match."
            )
            return

        try:
            success, message = db.register_user(
                fullname, username, email, password
            )

            if success:
                messagebox.showinfo(
                    "Success",
                    "Registration completed!\nPlease login now."
                )

                # IMPORTANT: Open login page after registration
                self.show_login(username)

            else:
                messagebox.showerror("Registration Error", message)

        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self.clear_screen()

        header = tk.Frame(self.root, bg="#154360")
        header.pack(fill="x")

        tk.Label(
            header,
            text="STUDENT MANAGEMENT SYSTEM",
            bg="#154360",
            fg="white",
            font=("Arial", 19, "bold")
        ).pack(side="left", padx=20, pady=22)

        tk.Button(
            header,
            text="LOGOUT",
            command=self.logout,
            bg="#c0392b",
            fg="white"
        ).pack(side="right", padx=20)

        tk.Label(
            self.root,
            text=f"Welcome, {self.fullname}",
            font=("Arial", 22, "bold"),
            bg="#eaf2f8",
            fg="#154360"
        ).pack(pady=35)

        tk.Label(
            self.root,
            text="Student Management Dashboard",
            font=("Arial", 14),
            bg="#eaf2f8"
        ).pack()

        cards = tk.Frame(self.root, bg="#eaf2f8")
        cards.pack(pady=65)

        self.button(
            cards, "ADD STUDENT", self.add_page, "#229954"
        ).pack(side="left", padx=10, ipady=20)

        self.button(
            cards, "VIEW STUDENTS", self.manage_page, "#2874a6"
        ).pack(side="left", padx=10, ipady=20)

        self.button(
            cards, "SEARCH STUDENTS", self.manage_page, "#8e44ad"
        ).pack(side="left", padx=10, ipady=20)

    # ---------------- STUDENT FORM ----------------

    def student_form(self, title, data=None):
        self.clear_screen()
        self.heading(title)

        frame = tk.Frame(
            self.root, bg="white", padx=45, pady=20
        )
        frame.pack(pady=25)

        self.entries = {}

        fields = [
            "Name", "Age", "Gender",
            "Course", "Email", "Phone"
        ]

        for i, field in enumerate(fields):
            tk.Label(
                frame, text=field, bg="white",
                font=("Arial", 10, "bold")
            ).grid(row=i, column=0, padx=15, pady=8, sticky="w")

            if field == "Gender":
                entry = ttk.Combobox(
                    frame,
                    values=["Male", "Female", "Other"],
                    state="readonly",
                    width=30
                )
            else:
                entry = tk.Entry(frame, width=33, font=("Arial", 11))

            entry.grid(row=i, column=1, padx=15, pady=8)

            if data and data[i] is not None:
                entry.insert(0, str(data[i]))

            self.entries[field] = entry

        label = "UPDATE STUDENT" if data else "SAVE STUDENT"

        self.button(
            frame, label, self.save_student, "#229954"
        ).grid(row=6, column=0, columnspan=2, pady=12)

        self.button(
            frame, "BACK TO DASHBOARD",
            self.show_dashboard, "#566573"
        ).grid(row=7, column=0, columnspan=2)

    # ---------------- ADD STUDENT ----------------

    def add_page(self):
        self.selected_id = None
        self.student_form("ADD NEW STUDENT")

    # ---------------- SAVE STUDENT ----------------

    def save_student(self):
        name = self.entries["Name"].get().strip()
        age_text = self.entries["Age"].get().strip()
        gender = self.entries["Gender"].get()
        course = self.entries["Course"].get().strip()
        email = self.entries["Email"].get().strip()
        phone = self.entries["Phone"].get().strip()

        if not name:
            messagebox.showerror("Error", "Enter student name.")
            return

        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            messagebox.showerror("Error", "Enter a valid student email.")
            return

        try:
            age = int(age_text) if age_text else None
            if age is not None and not 1 <= age <= 120:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid age.")
            return

        values = [name, age, gender, course, email, phone]

        try:
            if self.selected_id is None:
                db.add_student(self.user_id, values)
                messagebox.showinfo("Success", "Student added.")
            else:
                db.update_student(
                    self.selected_id, self.user_id, values
                )
                messagebox.showinfo("Success", "Student updated.")

            self.selected_id = None
            self.manage_page()

        except Exception as error:
            messagebox.showerror("Database Error", str(error))

    # ---------------- VIEW STUDENTS ----------------

    def manage_page(self):
        self.selected_id = None
        self.clear_screen()
        self.heading("STUDENT RECORDS")

        search_frame = tk.Frame(self.root, bg="#eaf2f8")
        search_frame.pack(pady=15)

        tk.Label(
            search_frame, text="Search:",
            bg="#eaf2f8"
        ).pack(side="left", padx=5)

        self.search_entry = tk.Entry(
            search_frame, width=28
        )
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="SEARCH",
            command=self.search_students,
            bg="#2874a6",
            fg="white"
        ).pack(side="left", padx=5)

        tk.Button(
            search_frame,
            text="SHOW ALL",
            command=self.load_students,
            bg="#566573",
            fg="white"
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.root)
        table_frame.pack(
            fill="both", expand=True,
            padx=20, pady=10
        )

        columns = (
            "ID", "Name", "Age", "Gender",
            "Course", "Email", "Phone"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=135, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        buttons = tk.Frame(self.root, bg="#eaf2f8")
        buttons.pack(pady=15)

        self.button(
            buttons, "ADD STUDENT", self.add_page, "#229954"
        ).pack(side="left", padx=7)

        self.button(
            buttons, "UPDATE", self.edit_student, "#2874a6"
        ).pack(side="left", padx=7)

        self.button(
            buttons, "DELETE", self.delete_student, "#c0392b"
        ).pack(side="left", padx=7)

        self.button(
            buttons, "DASHBOARD", self.show_dashboard, "#566573"
        ).pack(side="left", padx=7)

        self.load_students()

    # ---------------- LOAD RECORDS ----------------

    def load_students(self):
        self.display_records()

    def display_records(self, search=""):
        for item in self.table.get_children():
            self.table.delete(item)

        records = db.get_students(self.user_id, search)

        for record in records:
            self.table.insert("", tk.END, values=record)

    # ---------------- SEARCH ----------------

    def search_students(self):
        self.display_records(self.search_entry.get().strip())

    # ---------------- UPDATE ----------------

    def edit_student(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select a student first."
            )
            return

        data = self.table.item(selected[0])["values"]

        self.selected_id = data[0]
        self.student_form("UPDATE STUDENT", data[1:])

    # ---------------- DELETE ----------------

    def delete_student(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select a student first."
            )
            return

        data = self.table.item(selected[0])["values"]

        if messagebox.askyesno(
            "Confirm", "Delete this student?"
        ):
            try:
                db.delete_student(data[0], self.user_id)
                self.load_students()
                messagebox.showinfo(
                    "Success", "Student deleted."
                )
            except Exception as error:
                messagebox.showerror("Database Error", str(error))

    # ---------------- LOGOUT ----------------

    def logout(self):
        if messagebox.askyesno(
            "Logout", "Are you sure you want to logout?"
        ):
            self.user_id = None
            self.fullname = ""
            self.show_login()


# ---------------- START APPLICATION ----------------

if __name__ == "__main__":
    db.initialize_database()

    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()
