"""
Command-line entry point for the Secure Student Management System.

Can currently:
 - Register a new account
 - Log in with a stored account
 - Displays a dashboard for the active session. Currently empty.

Test logins:
 - Admin Email: admin@gmail.com, Admin Password: admin
 - User Email: test@gmail.com, User Password: password
 - John Email: jsmith@gmail.com, John Password: password
"""

from menu import main_menu

if __name__ == "__main__":
    main_menu()