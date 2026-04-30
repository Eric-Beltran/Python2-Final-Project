#reports.py
#This file creates CSV reports from database.json

import json
import csv


def load_database():
    #Open and read the database.json file
    with open("database.json", "r") as file:
        data = json.load(file)

    return data


def export_student_roster():
    #Load the data from database.json
    data = load_database()

    #Get the student list
    students = data["students"]

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
    #Load the data from database.json
    data = load_database()

    #Get the student list
    students = data["students"]

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