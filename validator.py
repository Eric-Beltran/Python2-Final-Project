"""
Runs only when registering a User
Contains Regex functions for names (capitalized, no digits),
phones (xxx-xxx-xxxx)
specific email extensions (.yahoo, .gmail, .ucmo).
And password format
"""

name_regex = r""
email_regex = r"(yahoo)(ucmo)(gmail)"
phone_regex = r"(\d{3}-\d{3}-\d{4})"
pass_regex = r"^[!@#$%^&*].*(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,11}$"