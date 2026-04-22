"""
"""

from analytics import display_grade_graphs
from data_handler import add_user, find_user_by, get_all_students, add_student, link_user_to_student, update_student, find_student_by, delete_student
from session_manager import login_session, logout_session, get_current_user
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Main menu
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

# Registration and Login function
def register():
    # Create a new user record if the email is not already registered.
    print("\n--- Register ---")
    email = input("Enter email: ")

    if find_user_by("email", email):
        print("User already exists.")
        return

    print("  \u2666 1. Password must start with one of the following special characters: !@#$%^&*")
    print("  \u2666 2. Password must contain at least one digit, one lowercase letter, and one uppercase letter.")
    print("  \u2666 3. Password is between 6 and 12 letters long.")
    password = input("Enter password: ")
    hashed = hash_password(password)

    # IMPORTANT!!! CHANGE THIS AT SOME POINT!!!
    # This is just a temporary measure so that we can test features that require the adminr role
    role_choice = input("Register as admin? (y/n): ").lower()

    if role_choice == "y":
        role = "admin"
    else:
        role = "user"

    user = {
        "email": email,
        "password": hashed,
        "role": role
    }

    add_user(user)
    print("Registration successful as {role}.")


def login():
    # Authenticate a user and start a session after a successful login
    attempts = 0

    while attempts < 3: # Someone should work on better security lmao. Also add regex
        print("\n--- Login ---")

        email = input("Enter email: ")
        password = input("Enter password: ")

        user = find_user_by("email", email)
        if user and user["password"] == hash_password(password):
            role = user["role"]
            login_session(user)
            print(f"Welcome, {email}. You are logged in as {role}.")
            dashboard()
            return

        attempts += 1
        print(f"Invalid login. Attempts left: {3 - attempts}")

    print("Too many failed attempts.")

# Gives admins the admin menu and regular users the regular menu
def dashboard():
    user = get_current_user()

    if user["role"] == "admin":
        admin_menu()
    else:
        user_menu()

# User menu
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

# Admin menu
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

# Functions for admin menu
def admin_add_student():
    print("\n--- Add Student ---")

    student_id = input("Enter student ID (700...): ")
    first = input("First name: ")
    last = input("Last name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    phone = input("Phone: ")
    major = input("Major: ")

    email = input("Enter user email to link: ")

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
        "grades": []
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
        updates["phone"] = new_phone

    if new_major:
        updates["major"] = new_major

    if update_student(student_id, updates):
        print("Student updated.")
    else:
        print("Update failed.")

def admin_view_students():
    students = get_all_students()

    for s in students:
        print(s)


def admin_delete_student():
    print("\n--- Delete Student ---")

    student_id = input("Enter student ID to delete: ")

    student = find_student_by("id", student_id)

    if not student:
        print("Student not found.")
        return

    # Show what you're about to delete
    print("\nStudent found:")
    print(f"{student['first_name']} {student['last_name']} (ID: {student['id']})")

    confirm = input("Are you sure you want to delete this student? (y/n): ").lower()

    if confirm != "y":
        print("Deletion cancelled.")
        return

    if delete_student(student_id):
        print("Student deleted successfully.")
    else:
        print("Error deleting student.")

# Functions for student menu
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