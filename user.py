"""
    • User (Base Class): Defines core attributes such as email and hashed password.
    • Admin(User): Inherits from User with full access to add, edit, and delete student data.
    • StudentUser(User): Inherits from User; restricted to view-only access
                        of their own specific records.
"""