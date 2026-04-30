"""
Menu flow for the Secure Student Management System.
"""

from analytics import display_grade_graphs
from data_handler import (
    add_student,
    create_student_record,
    delete_student,
    find_student_by,
    find_user_by,
    get_all_students,
    link_user_to_student,
    update_student,
)
from grade_manager import GradeManager
from session_manager import get_current_user, login_session, logout_session
from user import login_user, register_user
from validator import valid_email, valid_name, valid_password, valid_phone


def prompt_valid_input(prompt_text, validator, error_message):
    while True:
        value = input(prompt_text).strip()
        if validator(value):
            return value
        print(error_message)


def prompt_valid_age(prompt_text):
    while True:
        value = input(prompt_text).strip()
        if value.isdigit() and 16 <= int(value) <= 100:
            return int(value)
        print("Age must be a number between 16 and 100.")


def prompt_grade_row():
    while True:
        raw_value = input("Enter grades separated by commas: ").strip()
        if not raw_value:
            print("❗Please enter at least one grade.❗")
            continue

        parts = [part.strip() for part in raw_value.split(",")]
        grades = []

        for part in parts:
            if not part.isdigit():
                print("❗Grades must be whole numbers between 0 and 100.❗")
                break

            grade = int(part)
            if not 0 <= grade <= 100:
                print("❗Grades must be whole numbers between 0 and 100.❗")
                break

            grades.append(grade)
        else:
            return grades


def prompt_student_information():
    """
    Ask for the student fields that are needed for a student record.
    The ID is not asked for here because the system generates it automatically.
    """
    first = prompt_valid_input("First name: ", valid_name, "Invalid first name format.")
    last = prompt_valid_input("Last name: ", valid_name, "Invalid last name format.")
    age = prompt_valid_age("Age: ")
    gender = input("Gender: ").strip()
    phone = prompt_valid_input("Phone: ", valid_phone, "Invalid phone format.")
    major = input("Major: ").strip()

    return first, last, age, gender, phone, major


def print_student_record(student):
    """
    Print a student record in one place so admins and users see the same format.
    This also uses GradeManager to calculate the student's average.
    """
    for key, value in student.items():
        print(f"{key}: {value}")

    average = GradeManager.calculate_average(student.get("grades", []))
    print(f"average: {average:.2f}")


def main_menu():
    while True:
        print("\n🔒=== Secure Student Management System ===🔒")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("❗Invalid choice.❗")


def register():
    print("\n🔒--- Register ---🔒")
    email = prompt_valid_input("Enter email: ", valid_email, "Invalid email format.")

    if find_user_by("email", email):
        print("❗User already exists.❗")
        return

    print("1. Password must start with one of the following special characters: !@#$%^&*")
    print("2. Password must contain at least one digit, one lowercase letter, and one uppercase letter.")
    print("3. Password is between 6 and 12 letters long.")
    password = prompt_valid_input("Enter password: ", valid_password, "Invalid password format.")

    role_choice = input("Register as admin? (y/n): ").strip().lower()
    role = "admin" if role_choice == "y" else "user"

    if role == "admin":
        user = register_user(email=email, password=password, role=role)
        if not user:
            print("❗Registration failed.❗")
            return

        print("Registration successful as admin.")
        return

    print("\n--- Student Information ---")
    first, last, age, gender, phone, major = prompt_student_information()
    student = create_student_record(first, last, age, gender, phone, major)

    user = register_user(email=email, password=password, role=role, student_id=student["id"])
    if not user:
        print("❗Registration failed.❗")
        return

    if add_student(student):
        print("Registration successful as user.")
        print(f"Generated student ID: {student['id']}")
    else:
        print("User was created, but the student record could not be saved.")


def login():
    attempts = 0

    while attempts < 3:
        print("\n🔒--- Login ---🔒")
        email = prompt_valid_input("Enter email: ", valid_email, "Invalid email format.")
        password = input("Enter password: ")

        user = login_user(email, password)
        if user:
            login_session(user)
            print(f"Welcome, {email}. You are logged in as {user['role']}.")
            dashboard()
            return

        attempts += 1
        print(f"❗Invalid login. Attempts left: {3 - attempts}❗")

    print("❗Too many failed attempts.❗")


def dashboard():
    user = get_current_user()

    if user["role"] == "admin":
        admin_menu()
    else:
        user_menu()


def user_menu():
    while True:
        print("\n🔒--- User Dashboard ---🔒")
        print("1. View My Records")
        print("2. Logout")

        choice = input("Choose: ").strip()

        if choice == "1":
            view_my_record()
        elif choice == "2":
            logout_session()
            print("Logged out.")
            break
        else:
            print("❗Invalid choice.❗")


def admin_menu():
    while True:
        print("\n🔒--- Admin Dashboard ---🔒")
        print("➕1. Add Student")
        print("📝2. Edit Student")
        print("🔎3. View Students")
        print("🗑️4. Delete Student")
        print("📓5. Input Student Grades")
        print("📚6. View Grade Distribution")
        print("🚪7. Logout")

        choice = input("Choose: ").strip()

        if choice == "1":
            admin_add_student()
        elif choice == "2":
            admin_edit_student()
        elif choice == "3":
            admin_view_students()
        elif choice == "4":
            admin_delete_student()
        elif choice == "5":
            admin_input_grades()
        elif choice == "6":
            display_grade_graphs("database.json")
        elif choice == "7":
            logout_session()
            print("Logged out.")
            break
        else:
            print("❗Invalid choice.❗")


def admin_add_student():
    print("\n➕--- Add Student ---➕")

    first, last, age, gender, phone, major = prompt_student_information()
    email = prompt_valid_input("Enter user email to link: ", valid_email, "Invalid email format.")

    user = find_user_by("email", email)
    if not user:
        print("❗User not found. Create user first.❗")
        return

    if user.get("student_id"):
        print("❗This user is already linked to a student record.❗")
        return

    student = create_student_record(first, last, age, gender, phone, major)

    if add_student(student):
        link_user_to_student(email, student["id"])
        print("✅Student added and linked successfully.✅")
        print(f"✅Generated student ID: {student['id']}✅")
    else:
        print("❗Student could not be added.❗")


def admin_edit_student():
    print("\n📝--- Edit Student ---📝")

    student_id = input("Enter student ID: ").strip()
    student = find_student_by("id", student_id)

    if not student:
        print("❗Student not found.❗")
        return

    print("Leave blank to keep current value.")
    new_phone = input(f"Phone ({student['phone']}): ").strip()
    new_major = input(f"Major ({student['major']}): ").strip()

    updates = {}

    if new_phone:
        if not valid_phone(new_phone):
            print("❗Invalid phone format.❗")
            return
        updates["phone"] = new_phone

    if new_major:
        updates["major"] = new_major

    if update_student(student_id, updates):
        print("✅Student updated.✅")
    else:
        print("❗Update failed.❗")


def admin_view_students():
    students = get_all_students()

    if not students:
        print("❗No students found.❗")
        return

    for student in students:
        print("\n🎓--- Student Record ---🎓")
        print_student_record(student)


def admin_delete_student():
    print("\n🗑️--- Delete Student ---🗑️")

    student_id = input("Enter student ID to delete: ").strip()
    student = find_student_by("id", student_id)

    if not student:
        print("❗Student not found.❗")
        return

    print("\n✅Student found:✅")
    print(f"{student['first_name']} {student['last_name']} (ID: {student['id']})")

    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()
    if confirm != "y":
        print("Deletion cancelled.")
        return

    if delete_student(student_id):
        print("✅Student deleted successfully.✅")
    else:
        print("❗Error deleting student.❗")


def admin_input_grades():
    print("\n🎓--- Input Student Grades ---🎓")

    student_id = input("Enter student ID: ").strip()
    student = find_student_by("id", student_id)

    if not student:
        print("❗Student not found.❗")
        return

    print(f"Entering grades for {student['first_name']} {student['last_name']} (ID: {student['id']})")
    new_row = prompt_grade_row()
    updated_grades = [new_row]

    if update_student(student_id, {"grades": updated_grades}):
        average = GradeManager.calculate_average(updated_grades)
        print("✅Grades saved.✅")
        print(f"New average: {average:.2f}")
    else:
        print("❗Failed to save grades.❗")


def view_my_record():
    user = get_current_user()

    if not user.get("student_id"):
        print("❗No student record linked.❗")
        return

    student = find_student_by("id", user["student_id"])
    if not student:
        print("❗Student record not found.❗")
        return

    print("\n🔒--- My Student Record ---🔒")
    print_student_record(student)
