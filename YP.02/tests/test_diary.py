# tests/test_diary.py
import unittest
from database import add_subject, add_grade, get_grades_by_subject
from utils import calculate_average_grade
from datetime import date

class TestDiary(unittest.TestCase):
    def setUp(self):
        add_subject("Математика")
    
    def test_average_grade(self):
        subj = next(s for s in get_subjects() if s['name'] == "Математика")
        add_grade(subj['id'], date.today().isoformat(), 5, "Контрольная")
        add_grade(subj['id'], date.today().isoformat(), 4, "Самостоятельная")
        add_grade(subj['id'], date.today().isoformat(), 3, "")
        
        avg = calculate_average_grade(subj['id'])
        self.assertEqual(avg, 4.0)

if __name__ == '__main__':
    unittest.main()