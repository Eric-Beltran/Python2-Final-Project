"""
User models and authentication helpers.

This module defines regular and admin users, creates user dictionaries for
storage, registers new accounts, and verifies login attempts with salted
password hashes.
"""

from data_handler import add_user, find_user_by
from security import hash_password


class User:
    def __init__(self, email, hashed_password, role="user", student_id=None, salt=None):
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.student_id = student_id
        self.salt = salt

    def check_password(self, password):
        if self.salt is None:
            return False

        hashed_attempt, salt = hash_password(password, self.salt)
        return self.hashed_password == hashed_attempt

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.hashed_password,
            "salt": self.salt,
            "role": self.role,
            "student_id": self.student_id
        }


class Admin(User):
    def __init__(self, email, hashed_password, salt=None):
        super().__init__(
            email=email,
            hashed_password=hashed_password,
            role="admin",
            student_id=None,
            salt=salt
        )


class StudentUser(User):
    def __init__(self, email, hashed_password, student_id=None, salt=None):
        super().__init__(
            email=email,
            hashed_password=hashed_password,
            role="user",
            student_id=student_id,
            salt=salt
        )


def create_user_object(user_dict):
    email = user_dict.get("email")
    hashed_password = user_dict.get("password")
    role = user_dict.get("role")
    student_id = user_dict.get("student_id")
    salt = user_dict.get("salt")

    if role == "admin":
        return Admin(email, hashed_password, salt)

    return StudentUser(email, hashed_password, student_id, salt)


# ONLY CHANGED PART:
# Added student_id parameter so users can link to student records
def register_user(email, password, role="user", student_id=None):
    if find_user_by("email", email):
        return None

    hashed_password, salt = hash_password(password)

    if role == "admin":
        user_obj = Admin(email, hashed_password, salt)
    else:
        user_obj = StudentUser(
            email,
            hashed_password,
            student_id=student_id,
            salt=salt
        )

    user_dict = user_obj.to_dict()
    if not add_user(user_dict):
        return None

    return user_dict


def login_user(email, password):
    user_dict = find_user_by("email", email)

    if not user_dict:
        return None

    user_obj = create_user_object(user_dict)

    if user_obj.check_password(password):
        return user_obj.to_dict()

    return None


def is_admin(user):
    return user.get("role") == "admin"


def is_regular_user(user):
    return user.get("role") == "user"


def can_add_student(user):
    return is_admin(user)


def can_edit_student(user):
    return is_admin(user)


def can_delete_student(user):
    return is_admin(user)


def can_view_all_students(user):
    return is_admin(user)


def can_view_own_record(user):
    return is_regular_user(user)
