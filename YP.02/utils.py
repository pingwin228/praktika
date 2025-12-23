# utils.py
from datetime import date
from database import get_grades_by_subject

def calculate_average_grade(subject_id):
    grades = get_grades_by_subject(subject_id)
    if not grades:
        return 0.0
    total = sum(row['grade'] for row in grades)
    return round(total / len(grades), 2)

def calculate_overall_average():
    from database import get_all_grades
    all_grades = get_all_grades()
    if not all_grades:
        return 0.0
    total = sum(row['grade'] for row in all_grades)
    return round(total / len(all_grades), 2)

def is_overdue(homework):
    due = date.fromisoformat(homework['due_date'])
    return due < date.today() and homework['completed'] == 0