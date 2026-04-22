"""
Menu flow for the Secure Student Management System.
"""

from data_handler import (
    add_student,
    delete_student,
    find_student_by,
    find_user_by,
    get_all_students,
    link_user_to_student,
    update_student,
)
from session_manager import get_current_user, login_session, logout_session
from user import login_user, register_user
from validator import valid_email, valid_name, valid_password, valid_phone
from analytics import display_grade_graphs


def prompt_valid_input(prompt_text, validator, error_message):
    while True:
        value = input(prompt_text).strip()
        if validator(value):
            return value
        print(error_message)


def prompt_valid_age(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value.isdigit():
            return int(value)
        print("Age must be a number.")


def main_menu():
    while True:
        print("\n=== Secure Student Management System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")


def register():
    print("\n--- Register ---")
    email = prompt_valid_input("Enter email: ", valid_email, "Invalid email format.")

    if find_user_by("email", email):
        print("User already exists.")
        return

    print("  1. Password must start with one of the following special characters: !@#$%^&*")
    print("  2. Password must contain at least one digit, one lowercase letter, and one uppercase letter.")
    print("  3. Password is between 6 and 12 letters long.")
    password = prompt_valid_input("Enter password: ", valid_password, "Invalid password format.")

    role_choice = input("Register as admin? (y/n): ").strip().lower()
    role = "admin" if role_choice == "y" else "user"

    user = register_user(email=email, password=password, role=role)
    if not user:
        print("Registration failed.")
        return

    print(f"Registration successful as {role}.")


def login():
    attempts = 0

    while attempts < 3:
        print("\n--- Login ---")
        email = prompt_valid_input("Enter email: ", valid_email, "Invalid email format.")
        password = input("Enter password: ")

        user = login_user(email, password)
        if user:
            login_session(user)
            print(f"Welcome, {email}. You are logged in as {user['role']}.")
            dashboard()
            return

        attempts += 1
        print(f"Invalid login. Attempts left: {3 - attempts}")

    print("Too many failed attempts.")


def dashboard():
    user = get_current_user()

    if user["role"] == "admin":
        admin_menu()
    else:
        user_menu()


def user_menu():
    while True:
        print("\n--- User Dashboard ---")
        print("1. View My Records")
        print("2. Logout")

        choice = input("Choose: ")

        if choice == "1":
            view_my_record()
        elif choice == "2":
            logout_session()
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def admin_menu():
    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Add Student")
        print("2. Edit Student")
        print("3. View Students")
        print("4. Delete Student")
        print("5. View Grade Distribution")
        print("6. Logout")

        choice = input("Choose: ")

        if choice == "1":
            admin_add_student()
        elif choice == "2":
            admin_edit_student()
        elif choice == "3":
            admin_view_students()
        elif choice == "4":
            admin_delete_student()
        elif choice == "5":
            display_grade_graphs("database.json")
        elif choice == "6":
            logout_session()
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def admin_add_student():
    print("\n--- Add Student ---")

    student_id = input("Enter student ID (700...): ")
    first = prompt_valid_input("First name: ", valid_name, "Invalid first name format.")
    last = prompt_valid_input("Last name: ", valid_name, "Invalid last name format.")
    age = prompt_valid_age("Age: ")
    gender = input("Gender: ")
    phone = prompt_valid_input("Phone: ", valid_phone, "Invalid phone format.")
    major = input("Major: ")
    email = prompt_valid_input("Enter user email to link: ", valid_email, "Invalid email format.")

    user = find_user_by("email", email)
    if not user:
        print("User not found. Create user first.")
        return

    student = {
        "id": student_id,
        "first_name": first,
        "last_name": last,
        "age": age,
        "gender": gender,
        "phone": phone,
        "major": major,
        "grades": [],
    }

    add_student(student)
    link_user_to_student(email, student_id)

    print("Student added and linked successfully.")


def admin_edit_student():
    print("\n--- Edit Student ---")

    student_id = input("Enter student ID: ")
    student = find_student_by("id", student_id)

    if not student:
        print("Student not found.")
        return

    print("Leave blank to keep current value.")
    new_phone = input(f"Phone ({student['phone']}): ")
    new_major = input(f"Major ({student['major']}): ")

    updates = {}

    if new_phone:
        if not valid_phone(new_phone):
            print("Invalid phone format.")
            return
        updates["phone"] = new_phone

    if new_major:
        updates["major"] = new_major

    if update_student(student_id, updates):
        print("Student updated.")
    else:
        print("Update failed.")


def admin_view_students():
    students = get_all_students()
    for student in students:
        print(student)


def admin_delete_student():
    print("\n--- Delete Student ---")

    student_id = input("Enter student ID to delete: ")
    student = find_student_by("id", student_id)

    if not student:
        print("Student not found.")
        return

    print("\nStudent found:")
    print(f"{student['first_name']} {student['last_name']} (ID: {student['id']})")

    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    if delete_student(student_id):
        print("Student deleted successfully.")
    else:
        print("Error deleting student.")


def view_my_record():
    user = get_current_user()

    if not user.get("student_id"):
        print("No student record linked.")
        return

    student = find_student_by("id", user["student_id"])
    if not student:
        print("Student record not found.")
        return

    print("\n--- My Student Record ---")
    for key, value in student.items():
        print(f"{key}: {value}")
