class GradeManager:
    """
    This class handles student grades.
    Grades are stored as a 2D list.
    """

    @staticmethod
    def calculate_average(grades):
        # If there are no grades, return 0
        if not grades:
            return 0

        total = 0
        count = 0

        # Loop through each inner list
        for row in grades:
            # Loop through each grade inside that list
            for grade in row:
                total += grade
                count += 1

        if count == 0:
            return 0

        return total / count

    @staticmethod
    def add_grade_row(grades, new_row):
        # Add a whole new list of grades
        grades.append(new_row)
        return grades

    @staticmethod
    def add_single_grade(grades, grade):
        # If there isn't an inner list, make one
        if not grades:
            grades.append([])

        # Add one grade to the first inner list
        grades[0].append(grade)
        return grades