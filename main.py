import argparse
import openpyxl


def read_grades_from_csv(file_path: str):
    """Read and validate grades from a CSV file.
    Every line has a student ID of the form:
    111520YY00NNN
    where YY is the matriculation year and NNN is the student number.
    """
    lines = open(file_path, 'r').readlines()
    grades = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) != 2:
            raise ValueError(f"Invalid line format: {line}")

        student_id, grade_str = parts
        if not student_id.startswith("111520"):
            raise ValueError(f"Invalid student ID prefix: {student_id}")
        if len(student_id) < 13:
            raise ValueError(f"Student ID too short: {student_id}")
        if not student_id.isdigit():
            raise ValueError(f"Student ID must be numeric: {student_id}")
        if student_id[8:10] != "00":
            raise ValueError(f"Invalid student ID format (expected '00' at position 8-9): {student_id}")

        try:
            grade = int(grade_str)
        except ValueError:
            raise ValueError(f"Invalid grade for student {student_id}: {grade_str}")

        grades[student_id] = grade
    return grades


def apply_grades_to_xlsx(grades: dict, xlsx_file: str, debug: bool = False):
    """Matches the entry in the first column of the XLSX file with the student ID "Αριθμός Μητρώου" and adds the grade to the second column "Βαθμολογία"."""
    workbook = openpyxl.load_workbook(xlsx_file)
    sheet = workbook.active

    headers = True
    student_id_index = None
    grade_index = None
    applied_grades = 0
    total_students = 0
    for row in sheet.iter_rows(min_row=2, values_only=False):
        if headers:
            headers = False
            for cell in row:
                if cell.value == "Αριθμός Μητρώου":
                    student_id_index = cell.column - 1
                elif cell.value == "Βαθμολογία":
                    grade_index = cell.column - 1
            continue
        assert student_id_index is not None, "Student ID column not found."
        assert grade_index is not None, "Grade column not found."
        total_students += 1
        student_id_cell = row[student_id_index]
        grade_cell = row[grade_index]
        student_id = str(student_id_cell.value)
        if student_id in grades:
            grade = grades[student_id]
            if grade > 10:
                grade = 10
                print(f"Grade for student ID {student_id} capped at 10.")
            grade_cell.value = grade
            print(f"Applied grade {grade} to student ID {student_id}.")
            applied_grades += 1
        else:
            if debug:
                print(f"Student ID {student_id} not found in CSV file. Skipping.")
    print(f"Total students processed: {total_students}, Grades applied: {applied_grades}")
    workbook.save(xlsx_file)
    print(f"Grades applied to {xlsx_file} successfully.")


def main():
    parser = argparse.ArgumentParser(description="A script for adding grades from a CSV file to an XLSX file.")
    parser.add_argument(
        "csv_file",
        help="Path to the CSV file containing grades."
    )
    parser.add_argument(
        "xlsx_file",
        help="Path to the XLSX file where grades will be added."
    )
    parser.add_argument(
        "--only-passing",
        action="store_true",
        help="If set, only passing grades will be added to the XLSX file."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode for additional output."
    )
    args = parser.parse_args()

    grades = read_grades_from_csv(args.csv_file)
    if args.only_passing:
        grades = {k: v for k, v in grades.items() if v >= 5}
    apply_grades_to_xlsx(grades, args.xlsx_file, debug=args.debug)


if __name__ == "__main__":
    main()
