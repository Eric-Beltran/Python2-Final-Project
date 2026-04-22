"""
Identity layer for the Secure Student Management System.
"""

from data_handler import add_user, find_user_by
from security import hash_password
from validator import valid_email, valid_password


class User:
    def __init__(self, email, hashed_password, role="user", student_id=None):
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.student_id = student_id

    def check_password(self, password):
        return self.hashed_password == hash_password(password)

    def get_role(self):
        return self.role

    def can_view_own_record(self):
        return True

    def can_view_all_students(self):
        return False

    def can_add_student(self):
        return False

    def can_edit_student(self):
        return False

    def can_delete_student(self):
        return False

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.hashed_password,
            "role": self.role,
            "student_id": self.student_id,
        }


class Admin(User):
    def __init__(self, email, hashed_password):
        super().__init__(email, hashed_password, role="admin", student_id=None)

    def can_view_all_students(self):
        return True

    def can_add_student(self):
        return True

    def can_edit_student(self):
        return True

    def can_delete_student(self):
        return True


class StudentUser(User):
    def __init__(self, email, hashed_password, student_id=None):
        super().__init__(email, hashed_password, role="user", student_id=student_id)


def create_user_object(user_dict):
    role = user_dict.get("role")
    email = user_dict.get("email")
    hashed_password = user_dict.get("password") or user_dict.get("hashed_password")
    student_id = user_dict.get("student_id")

    if role == "admin":
        return Admin(email, hashed_password)

    return StudentUser(email, hashed_password, student_id)


def register_user(email, password, role="user", student_id=None):
    if not valid_email(email) or not valid_password(password):
        return None

    if find_user_by("email", email):
        return None

    if role == "admin":
        new_user = Admin(email, hash_password(password))
    elif role == "user":
        new_user = StudentUser(email, hash_password(password), student_id)
    else:
        return None

    user_dict = new_user.to_dict()
    add_user(user_dict)
    return user_dict


def login_user(email, password):
    user_dict = find_user_by("email", email)
    if not user_dict:
        return None

    user_obj = create_user_object(user_dict)
    if user_obj.check_password(password):
        return user_obj.to_dict()

    return None
