"""
Input validation helpers for the CLI.

These functions validate names, email addresses, phone numbers, and passwords
before registration or student-record updates are allowed to continue.
"""
import re

def valid_name(name):
    name_regex = r"^[A-Z][a-z]{2,}$"
    if re.match(name_regex, name):
        return True
    return False

def valid_email(email):
    email_regex = r"^[A-Za-z0-9._%+-]+@(gmail\.com|yahoo\.com|ucmo\.edu)$"
    if re.match(email_regex, email):
        return True
    return False

def valid_phone(phone):
    phone_regex = r"^\d{3}-\d{3}-\d{4}$"
    if re.match(phone_regex, phone):
        return True
    return False

def valid_password(password):
    pass_regex = r"^(?=.{6,12}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[!@#$%^&*].*$"
    if re.match(pass_regex, password):
        return True
    return False
