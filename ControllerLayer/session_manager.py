"""
Tracks the currently logged-in user for the session.
"""

current_user = None


def login_session(user):
    # Store the authenticated user as the active session
    global current_user
    current_user = user


def logout_session():
    # Clear the active session
    global current_user
    current_user = None


def get_current_user():
    # Return the active user, or None if nobody is logged in
    return current_user
