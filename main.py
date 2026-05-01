"""
Command-line entry point for the Secure Student Management System.

This file configures the CLI to use the remote API by default, checks whether
the API and database are reachable, and then starts the main menu.

Test logins:
 - Admin Email: admin@gmail.com, Admin Password: !1Password
"""

import os

os.environ.setdefault("USE_REMOTE_API", "1")

from menu import main_menu


def check_remote_api():
    if os.environ.get("USE_REMOTE_API", "1") != "1":
        return

    import api_client

    if not api_client.health_check():
        print(f"Warning: Could not reach API server at {api_client.API_BASE}.")
        return

    database_ok, response = api_client.database_health_check()
    if not database_ok:
        error = response.get("error") if isinstance(response, dict) else "unknown database error"
        print(f"Warning: API server cannot reach DynamoDB: {error}")


if __name__ == "__main__":
    check_remote_api()
    main_menu()
