"""
    • User (Base Class): Defines core attributes such as email and hashed password.
    • Admin(User): Inherits from User with full access to add, edit, and delete student data.
    • StudentUser(User): Inherits from User; restricted to view-only access
                        of their own specific records.
"""
"""
user.py
Identity layer for the Secure Student Management System.

This file contains the User base class and two child classes:
Admin and StudentUser.

It also contains helper functions for:
- registering a new user
- logging in a user
- converting users to and from dictionary format

This file should work with:
- validator.py
- security.py
- data_handler.py
"""

from validator import valid_email, valid_password
from security import hash_password
from data_handler import load_data, save_data


class User:
    """
    Base User class.
    Stores the email, hashed password, role, and optional student ID.
    """

    def __init__(self, email, hashed_password, role="user", student_id=None):
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.student_id = student_id

    def check_password(self, password):
        """
        Compare the hashed version of the input password
        to the stored hashed password.
        """
        return self.hashed_password == hash_password(password)

    def get_role(self):
        """
        Return the role of the user.
        """
        return self.role

    def can_view_own_record(self):
        """
        All users can view their own record.
        """
        return True

    def can_view_all_students(self):
        """
        Base users cannot view all student records.
        """
        return False

    def can_add_student(self):
        """
        Base users cannot add student records.
        """
        return False

    def can_edit_student(self):
        """
        Base users cannot edit student records.
        """
        return False

    def can_delete_student(self):
        """
        Base users cannot delete student records.
        """
        return False

    def to_dict(self):
        """
        Convert the user object into dictionary format
        so it can be stored in database.json.
        """
        return {
            "email": self.email,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "student_id": self.student_id
        }


class Admin(User):
    """
    Admin child class.
    Admin has full access to student records.
    """

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
    """
    StudentUser child class.
    Student users are limited to viewing only their own record.
    """

    def __init__(self, email, hashed_password, student_id):
        super().__init__(email, hashed_password, role="user", student_id=student_id)


def create_user_object(user_dict):
    """
    Take a dictionary from database.json and turn it into
    the correct object type.
    """
    role = user_dict.get("role")
    email = user_dict.get("email")
    hashed_password = user_dict.get("hashed_password")
    student_id = user_dict.get("student_id")

    if role == "admin":
        return Admin(email, hashed_password)
    else:
        return StudentUser(email, hashed_password, student_id)


def email_exists(email, users_list):
    """
    Check if an email already exists in the users list.
    """
    for user in users_list:
        if user.get("email") == email:
            return True
    return False


def register_user():
    """
    Register a new user and save them into database.json.

    Returns:
        User object if registration is successful
        None if registration fails
    """
    data = load_data()

    if "users" not in data:
        data["users"] = []

    email = input("Enter email: ").strip()

    if not valid_email(email):
        print("Invalid email. Use only .gmail, .yahoo, or .ucmo")
        return None

    if email_exists(email, data["users"]):
        print("That email is already registered.")
        return None

    password = input("Enter password: ").strip()

    if not valid_password(password):
        print("Invalid password.")
        print("Password must:")
        print("- start with !@#$%^&*")
        print("- be 6 to 12 characters long")
        print("- contain at least 1 uppercase letter")
        print("- contain at least 1 lowercase letter")
        print("- contain at least 1 digit")
        return None

    role = input("Enter role (admin/user): ").strip().lower()

    if role == "admin":
        new_user = Admin(email, hash_password(password))
    elif role == "user":
        student_id = input("Enter linked student 700 number: ").strip()
        new_user = StudentUser(email, hash_password(password), student_id)
    else:
        print("Invalid role.")
        return None

    data["users"].append(new_user.to_dict())
    save_data(data)

    print("Registration successful.")
    return new_user


def login_user():
    """
    Log in a user by checking email and password.

    Returns:
        User object if login is successful
        None if login fails
    """
    data = load_data()

    if "users" not in data:
        print("No users found in the system.")
        return None

    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    for user_dict in data["users"]:
        if user_dict.get("email") == email:
            user_obj = create_user_object(user_dict)

            if user_obj.check_password(password):
                print("Login successful.")
                return user_obj
            else:
                print("Incorrect password.")
                return None

    print("Account not found.")
    return None
