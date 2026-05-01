"""
Command-line entry point for the Secure Student Management System.

Can currently:
 - Register a new account
 - Log in with a stored account
 - Displays a dashboard for the active session. Currently empty.

Test logins:
 - Admin Email: admin@gmail.com, Admin Password: !1Password
"""

import os

os.environ.setdefault("USE_REMOTE_API", "1")

from menu import main_menu

if __name__ == "__main__":
    main_menu()
