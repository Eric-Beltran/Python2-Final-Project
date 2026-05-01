"""
CSV export functions for student data.

The admin menu calls this module to create roster and report-card files from
the same student records used by the rest of the application.
"""

import csv
from data_handler import get_all_students


def load_students():
    # Read student data through data_handler so reports use the same DynamoDB path.
    return get_all_students()


def export_student_roster():
    students = load_students()

    #Create the CSV file
    with open("student_roster.csv", "w", newline="") as file:
        writer = csv.writer(file)

        #Column headers
        writer.writerow(["Student ID", "First Name", "Last Name", "Age", "Gender", "Grades"])

        #Write each student into the CSV
        for student in students:
            writer.writerow([
                student.get("id", ""),
                student.get("first_name", ""),
                student.get("last_name", ""),
                student.get("age", ""),
                student.get("gender", ""),
                student.get("grades", "")
            ])

    print("Student roster exported successfully as student_roster.csv")


def export_report_cards():
    students = load_students()

    #Create the CSV file
    with open("report_cards.csv", "w", newline="") as file:
        writer = csv.writer(file)

        #Column headers
        writer.writerow(["Student ID", "Student Name", "Grades"])

        #Write each report card row
        for student in students:
            full_name = student.get("first_name", "") + " " + student.get("last_name", "")

            writer.writerow([
                student.get("id", ""),
                full_name,
                student.get("grades", "")
            ])

    print("Report cards exported successfully as report_cards.csv")
