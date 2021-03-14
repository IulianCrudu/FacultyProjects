from datetime import datetime
from uuid import uuid4
import unittest
from faker import Faker

from src.domain import Assignment
from src.repository import Repository
from src.service.assignment_service import AssignmentService, AssignmentServiceException
from src.validators import AssignmentValidatorException, AssignmentValidator


class TestAssignment(unittest.TestCase):
    def setUp(self):
        assignment_repo = Repository(pk="assignment_id")
        self.assignment_service = AssignmentService(repo=assignment_repo, validator=AssignmentValidator)

    @staticmethod
    def get_random_id():
        return str(uuid4().fields[-1])[:8]

    @staticmethod
    def load_fixtures(assignment_repo, nr: int = 10):
        fake = Faker()
        for i in range(nr):
            assignment_id = TestAssignment.get_random_id()
            description = fake.sentence(nb_words=10)
            deadline = fake.date_time()
            assignment = Assignment(assignment_id, description, deadline)
            assignment_repo.add_item(assignment)

    def test_add_assignment(self):
        assignment_service = self.assignment_service
        TestAssignment.load_fixtures(assignment_service.repo, 2)
        self.assertEqual(len(assignment_service.repo), 2)

        assignment_service.add_assignment("assignment_1", "Description", "20-12-2020 20:45")

        self.assertEqual(len(assignment_service.repo), 3)
        last_assignment = assignment_service.get_all_assignments()[-1]
        self.assertEqual(last_assignment.assignment_id, "assignment_1")
        self.assertEqual(last_assignment.description, "Description")
        self.assertEqual(last_assignment.deadline, datetime.strptime("20-12-2020 20:45", "%d-%m-%Y %H:%M"))

        try:
            # Test that we can't have assignments with the same id
            assignment_service.add_assignment("assignment_1", "test desc", "20-12-2020 20:45")
            self.assertTrue(False)
        except AssignmentValidatorException:
            self.assertTrue(True)

        try:
            # Test that id needs tobe string
            assignment_service.add_assignment(123, "test desc", "20-12-2020 20:45")
            self.assertTrue(False)
        except AssignmentValidatorException:
            self.assertTrue(True)

    def test_remove_works(self):
        assignment_service = self.assignment_service
        TestAssignment.load_fixtures(assignment_service.repo, 5)
        self.assertEqual(len(assignment_service.repo), 5)

        valid_id = assignment_service.get_all_assignments()[-1].assignment_id
        assignment_service.remove_assignment(valid_id)
        self.assertEqual(len(assignment_service.repo), 4)
        self.assertFalse([
            assignment for assignment in assignment_service.get_all_assignments()
            if assignment.assignment_id == valid_id
        ])

        try:
            assignment_service.remove_assignment("random id")
            self.assertTrue(False)
        except AssignmentServiceException:
            self.assertTrue(True)

    def test_update_works(self):
        assignment_service = self.assignment_service
        TestAssignment.load_fixtures(assignment_service.repo, 5)
        self.assertEqual(len(assignment_service.repo), 5)

        assignment = assignment_service.get_all_assignments()[-1]
        assignment_service.update_assignment(assignment.assignment_id, description="New Description")
        self.assertEqual(assignment.description, "New Description")
        assignment_service.update_assignment(assignment.assignment_id, deadline="25-12-2020 21:00")
        self.assertEqual(assignment.deadline, datetime.strptime("25-12-2020 21:00", "%d-%m-%Y %H:%M"))

        try:
            assignment_service.update_assignment("random id", description="New Description")
            self.assertTrue(False)
        except AssignmentServiceException:
            self.assertTrue(True)
