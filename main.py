"""
Command-line entry point for the Secure Student Management System.

Can currently:
 - Register a new account
 - Log in with a stored account
 - Displays a dashboard for the active session. Currently empty.
"""

import hashlib

from ControllerLayer.session_manager import (
    get_current_user,
    login_session,
    logout_session,
)
from StorageLayer.data_handler import add_user, find_user

def hash_password(password):
    # Return SHA-256 hash so plain-text passwords are never stored
    # Something like this should be moved to the security layer file handling hashing later
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    # Create a new user record if the email is not already registered.
    print("\n--- Register ---")
    email = input("Enter email: ")

    if find_user(email):
        print("User already exists.")
        return

    password = input("Enter password: ")
    hashed = hash_password(password)

    user = {
        "email": email,
        "password": hashed,
        "role": "user",
    }

    add_user(user)
    print("Registration successful.")


def login():
    # Authenticate a user and start a session after a successful login
    print("\n--- Login ---")

    attempts = 0

    while attempts < 3: # Someone should work on better security lmao. Also add regex
        email = input("Enter email: ")
        password = input("Enter password: ")

        user = find_user(email)

        if user and user["password"] == hash_password(password):
            login_session(user)
            print(f"Welcome, {email}")
            return

        attempts += 1
        print(f"Invalid login. Attempts left: {3 - attempts}")

    print("Too many failed attempts.")


def dashboard():
    # Show the post-login menu for the current user
    user = get_current_user()

    if not user:
        return

    while True:
        print("\n--- Dashboard ---")
        print("1. Logout")

        choice = input("Choose: ")

        if choice == "1":
            logout_session()
            print("Logged out.")
            break

        print("Invalid option.")


def main():
    # Keep the app running until the user chooses to exit.
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
            if get_current_user():
                dashboard()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
