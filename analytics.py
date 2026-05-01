'''
Using matplotlib to create data visualization graphics specifically for
student grades.

'''

from data_handler import get_all_students
from grade_manager import GradeManager


def display_grade_graphs():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Matplotlib is not installed, so grade graphs cannot be displayed.")
        return

    students = get_all_students()

    if not students:
        print("No students found.")
        return

    # lists to store results
    student_names = []
    student_averages = []

    # function to convert to letter grades
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

    # grade distribution dictionary
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

    # process each student
    for student in students:
        full_name = student["first_name"] + " " + student["last_name"]
        avg = GradeManager.calculate_average(student.get("grades", []))

        student_names.append(full_name)
        student_averages.append(avg)

        # update distribution
        letter = get_letter_grade(avg)
        grade_counts[letter] += 1

    # print results
    print("\nStudent Averages:")
    for i in range(len(student_names)):
        print(student_names[i] + ": " + str(round(student_averages[i], 2)))

    # bar chart: student averages
    plt.figure()
    plt.bar(student_names, student_averages)
    plt.title("Student Average Grades")
    plt.xlabel("Students")
    plt.ylabel("Average Grade")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # bar chart: grade distribution
    plt.figure()
    plt.bar(list(grade_counts.keys()), list(grade_counts.values()))
    plt.title("Grade Distribution")
    plt.xlabel("Letter Grade")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.show()

    # histogram: averages
    plt.figure()
    plt.hist(student_averages, bins=10)
    plt.title("Distribution of Student Averages")
    plt.xlabel("Average Grade")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

    # pie chart: percentage distribution
    plt.figure()
    plt.pie(list(grade_counts.values()), labels=list(grade_counts.keys()), autopct="%1.1f%%")
    plt.title("Grade Distribution Percentage")
    plt.show()
