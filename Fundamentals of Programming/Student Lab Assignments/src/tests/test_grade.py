import unittest
from uuid import uuid4
from random import choice

from src.domain import Grade
from src.repository import Repository, GradeRepository
from src.service import GradeService
from src.validators import GradeValidator


grade_values = [0, 3, 7, 10]


class TestGrade(unittest.TestCase):
    @staticmethod
    def load_fixtures(grade_repo, student_repo, assignment_repo, nr: int = 10):
        for i in range(nr):
            student = student_repo.items[i]
            assignment = assignment_repo.items[i]
            grade_value = choice([0, choice(grade_values)])
            grade = Grade(
                assignment_id=assignment.assignment_id,
                student_id=student.student_id,
                grade_value=grade_value
            )
            grade_repo.add_item(grade)

    def setUp(self):
        grade_repository = GradeRepository()
        student_repository = Repository(pk="student_id")
        assignment_repository = Repository(pk="assignment_id")
        self.grade_service = GradeService(
            grade_repo=grade_repository,
            assignment_repo=assignment_repository,
            student_repo=student_repository,
            validator=GradeValidator
        )

    def test_assign_to_student(self):
        grade_service = self.grade_service
        self.assertTrue(True)
