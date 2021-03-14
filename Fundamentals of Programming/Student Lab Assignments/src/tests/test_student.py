from uuid import uuid4
from random import choice
import unittest
from faker import Faker

from src.domain import Student
from src.repository import Repository
from src.service.student_service import StudentService, StudentServiceException
from src.service import UndoService
from src.validators import StudentValidatorException, StudentValidator

group_list = ["911", "912", "913", "915", "916"]


class TestStudent(unittest.TestCase):
    @staticmethod
    def get_random_id():
        return str(uuid4().fields[-1])[:8]

    @staticmethod
    def load_fixtures(student_repo, nr: int = 10):
        fake = Faker()
        for i in range(nr):
            student_id = TestStudent.get_random_id()
            name = fake.name()
            group = choice(group_list)
            student = Student(student_id, name, group)
            student_repo.add_item(student)

    def setUp(self):
        student_repo = Repository(pk="student_id")
        undo_service = UndoService()
        self.student_service = StudentService(repo=student_repo, validator=StudentValidator, undo_service=undo_service)

    def test_add_works(self):
        TestStudent.load_fixtures(self.student_service.repo, 2)
        assert len(self.student_service.repo) == 2

        self.student_service.add_student("abc", "test name", "test group")
        assert len(self.student_service.repo) == 3
        last_student = self.student_service.repo.items[-1]
        self.assertEqual(last_student.student_id, "abc")
        self.assertEqual(last_student.name, "test name")
        self.assertEqual(last_student.group, "test group")

        try:
            # Test that we can't have students with the same id
            self.student_service.add_student("abc", "test name", "test group")
            self.assertTrue(False)
        except StudentValidatorException:
            self.assertTrue(True)

        try:
            # Test that id needs tobe string
            self.student_service.add_student(123, "test name", "test group")
            self.assertTrue(False)
        except StudentValidatorException:
            self.assertTrue(True)

    def test_remove_works(self):
        student_service = self.student_service
        TestStudent.load_fixtures(student_service.repo, 5)
        self.assertEqual(len(student_service.repo), 5)

        valid_id = student_service.get_all_students()[-1].student_id
        student_service.remove_student(valid_id)
        self.assertEqual(len(student_service.repo), 4)
        self.assertFalse([student for student in student_service.get_all_students() if student.student_id == valid_id])

        try:
            student_service.remove_student("random id")
            self.assertTrue(False)
        except StudentServiceException:
            self.assertTrue(True)

    def test_update_works(self):
        student_service = self.student_service
        TestStudent.load_fixtures(student_service.repo, 5)
        self.assertEqual(len(student_service.repo), 5)

        student = student_service.get_all_students()[-1]
        student_service.update_student(student.student_id, name="New Name")
        self.assertEqual(student.name, "New Name")
        student_service.update_student(student.student_id, group="New Group")
        self.assertEqual(student.group, "New Group")

        try:
            student_service.update_student("random id", name="New Name")
            self.assertTrue(False)
        except StudentServiceException:
            self.assertTrue(True)
