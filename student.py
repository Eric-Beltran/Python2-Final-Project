"""
Student record model.

StudentRecord stores the fields used by the database and menus, then converts
between object form and dictionary form for persistence and display.
"""

class StudentRecord:
    """
    This class stores the information for one student.

    The project already uses "id" for student records, so this class keeps that
    same naming style instead of changing it to something else.
    """

    def __init__(self, student_id, first_name, last_name, age, gender, phone, major="", grades=None):
        self.id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.major = major
        self.grades = grades if grades is not None else []

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def to_dict(self):
        # This converts the object into the same dictionary format the database uses
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "major": self.major,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data):
        # This rebuilds a StudentRecord object from a dictionary loaded from JSON
        return cls(
            data["id"],
            data["first_name"],
            data["last_name"],
            data["age"],
            data["gender"],
            data["phone"],
            data.get("major", ""),
            data.get("grades", [])
        )

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"Name: {self.get_full_name()}, "
            f"Age: {self.age}, "
            f"Gender: {self.gender}, "
            f"Phone: {self.phone}, "
            f"Major: {self.major}, "
            f"Grades: {self.grades}"
        )
