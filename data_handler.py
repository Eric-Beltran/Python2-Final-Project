import json
from pathlib import Path

DATABASE_FILE = Path(__file__).resolve().parent / "database.json"
EMPTY_DATABASE = {"users": [], "students": []}


def load_data():
    # Load the JSON database, creating an empty one if needed
    try:
        if not DATABASE_FILE.exists():
            with DATABASE_FILE.open("w", encoding="utf-8") as file:
                json.dump(EMPTY_DATABASE, file, indent=4)

        with DATABASE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except json.JSONDecodeError:
        print("Error: JSON file is corrupted. Resetting database.")
        return EMPTY_DATABASE.copy()

    except Exception as error:
        print(f"Unexpected error: {error}")
        return EMPTY_DATABASE.copy()


def save_data(data):
    # Persist the in-memory database back to the JSON file
    try:
        with DATABASE_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except Exception as error:
        print(f"Error saving data: {error}")


def add_user(user):
    # Append a user to the database
    data = load_data()
    data["users"].append(user)
    save_data(data)


def find_user_by(field, value):
    # Searches a user by specified field
    data = load_data()

    for user in data["users"]:
        if user.get(field) == value:
            return user

    return None


def find_student_by(field, value):
    # Searches a student by specified field
    data = load_data()

    for student in data["students"]:
        if student.get(field) == value:
            return student

    return None

def add_student(student):
    # Append a student to the database
    data = load_data()
    data["students"].append(student)
    save_data(data)

def update_student(student_id, updated_data):
    data = load_data()

    for student in data["students"]:
        if student["id"] == student_id:
            student.update(updated_data)
            save_data(data)
            return True

    return False

def get_all_students():
    # Return all student data currently stored
    data = load_data()
    return data["students"]


def delete_student(student_id):
    data = load_data()

    student_exists = False

    # Remove student
    new_students = []
    for student in data["students"]:
        if student["id"] == student_id:
            student_exists = True
        else:
            new_students.append(student)

    if not student_exists:
        return False

    data["students"] = new_students

    # Unlink any user connected to this student
    for user in data["users"]:
        if user.get("student_id") == student_id:
            user["student_id"] = None

    save_data(data)
    return True

def link_user_to_student(email, student_id):
    data = load_data()

    for user in data["users"]:
        if user["email"] == email:
            user["student_id"] = student_id
            save_data(data)
            return True

    return False
