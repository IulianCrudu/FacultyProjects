from typing import List
from datetime import datetime


class AssignmentValidatorException(Exception):
    def __init__(self, msg):
        self._msg = msg


class AssignmentValidator:
    @staticmethod
    def is_id_used(assignment_list: List, assignment_id: str):
        return bool([assignment for assignment in assignment_list if assignment.assignment_id == assignment_id])

    @staticmethod
    def validate_id_unique(assignment_list: List, assignment_id: str):
        if AssignmentValidator.is_id_used(assignment_list, assignment_id):
            raise AssignmentValidatorException(f"Assignment with id={assignment_id} exists.")

    @staticmethod
    def validate_assignment_id(assignment_list: List, assignment_id: str):
        if not isinstance(assignment_id, str):
            raise AssignmentValidatorException("Assignment's ID must be a string.")
        AssignmentValidator.validate_id_unique(assignment_list, assignment_id)

    @staticmethod
    def validate_description(description: str):
        if not isinstance(description, str):
            raise AssignmentValidatorException("Assignment's description must be a string.")

    @staticmethod
    def validate_deadline(deadline: datetime):
        if not isinstance(deadline, datetime):
            raise AssignmentValidatorException("Assignment's deadline must be a datetime instance.")

    @staticmethod
    def validate_deadline_str(deadline: str):
        # Deadline should have this format: dd-mm-yyyy hh:mm
        date_format = "%d-%m-%Y %H:%M"

        if not datetime.strptime(deadline, date_format):
            raise AssignmentValidatorException("Assignment's deadline doesn't have the right format.")

    @staticmethod
    def validate_assignment(assignment_list: List, assignment_id: str, description: str, deadline: str):
        AssignmentValidator.validate_assignment_id(assignment_list, assignment_id)
        AssignmentValidator.validate_description(description)
        AssignmentValidator.validate_deadline_str(deadline)
