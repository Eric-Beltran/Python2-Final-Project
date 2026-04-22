'''
Using matplotlib to create data visualization graphics specifically for
student grades.

Pulls directly from database.json
'''

import json
import matplotlib.pyplot as plt

def display_grade_graohs(filename):
    with open(filename, "r") as file:
        data = json.load(file)

        students = data["students"]

        student_names = []
        student_averages = []

        def get_letter_grade(avg):
            if avg >= 90:
                return "A"
            elif avg >= 80:
                return "B"
            elif avg >= 70:
                return "C"
            elif avg >= 60:
                return "D"
            else:
                return "F"

        grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

        for student in students:
            full_name = student["First Name"] + " " + student["Last Name"]

