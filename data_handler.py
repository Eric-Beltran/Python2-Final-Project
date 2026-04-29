import json
import random
from pathlib import Path
from student import StudentRecord

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

        # Make sure both main keys exist even if the JSON file is missing one
        data.setdefault("users", [])
        data.setdefault("students", [])
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


def update_user(email, updated_data):
    data = load_data()

    for user in data["users"]:
        if user["email"] == email:
            user.update(updated_data)
            save_data(data)
            return True

    return False


def find_student_by(field, value):
    # Searches a student by specified field
    data = load_data()

    for student in data["students"]:
        if student.get(field) == value:
            return student

    return None


def get_existing_student_ids():
    # Store existing IDs in a set so checking duplicates is fast
    data = load_data()
    return {student.get("id") for student in data["students"]}


def generate_student_id():
    """
    Generate a unique random 700###### ID.
    Example: 700717441
    """
    existing_ids = get_existing_student_ids()

    while True:
        student_id = "700" + str(random.randint(100000, 999999))

        if student_id not in existing_ids:
            return student_id


def create_student_record(first_name, last_name, age, gender, phone, major="", grades=None, student_id=None):
    """
    Create a student dictionary using the StudentRecord class.
    This keeps the database naming style the same, especially using "id".
    """
    if student_id is None:
        student_id = generate_student_id()

    student = StudentRecord(
        student_id,
        first_name,
        last_name,
        int(age),
        gender,
        phone,
        major,
        grades if grades is not None else []
    )

    return student.to_dict()


def add_student(student):
    # Append a student to the database
    data = load_data()

    # If no ID was provided, generate one automatically
    if not student.get("id"):
        student["id"] = generate_student_id()

    # Do not allow duplicate student IDs
    if find_student_by("id", student["id"]):
        print("Error: A student with this ID already exists.")
        return False

    data["students"].append(student)
    save_data(data)
    return True


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
