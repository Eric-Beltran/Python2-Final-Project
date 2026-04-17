"""Read and write the project's JSON-backed storage."""

import json
from pathlib import Path

DATABASE_FILE = Path(__file__).resolve().parent.parent / "database.json"
EMPTY_DATABASE = {"users": [], "students": []}


def load_data():
    """Load the JSON database, creating an empty one if needed."""
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
    """Persist the in-memory database back to the JSON file."""
    try:
        with DATABASE_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except Exception as error:
        print(f"Error saving data: {error}")


def add_user(user):
    """Append a user record to the database."""
    data = load_data()
    data["users"].append(user)
    save_data(data)


def find_user(email):
    """Return the user record for the given email, if one exists."""
    data = load_data()

    for user in data["users"]:
        if user["email"] == email:
            return user

    return None


def add_student(student):
    """Append a student record to the database."""
    data = load_data()
    data["students"].append(student)
    save_data(data)


def get_all_students():
    """Return all student records currently stored."""
    data = load_data()
    return data["students"]


def delete_student(student_id):
    """Remove a student record by its ID."""
    data = load_data()
    data["students"] = [
        student for student in data["students"] if student["id"] != student_id
    ]
    save_data(data)
