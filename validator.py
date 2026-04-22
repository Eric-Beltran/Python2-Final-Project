"""
Runs only when registering a User
Contains Regex functions for names (capitalized, no digits),
phones (xxx-xxx-xxxx)
specific email extensions (@yahoo, @gmail, @ucmo).
And password format
"""
import re

def valid_name(name):
    name_regex = r"(^[A-Z])([a-z]{2,})"
    if re.match(name_regex, name):
        return True
    return False

def valid_email(email):
    email_regex = r"(@yahoo\.|@ucmo\.|@gmail\.)"
    if re.match(email_regex, email):
        return True
    return False

def valid_phone(phone):
    phone_regex = r"(\d{3}-\d{3}-\d{4})"
    if re.match(phone_regex, phone):
        return True
    return False

def valid_password(password):
    pass_regex = r"^[!@#$%^&*].*(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,11}$"
    if re.match(pass_regex, password):
        return True
    return False