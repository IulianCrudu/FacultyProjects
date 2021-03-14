from typing import List, Optional

from .assignment_validator import AssignmentValidator
from .student_validator import StudentValidator


class GradeValidatorException(Exception):
    def __init__(self, msg):
        self._msg = msg


class GradeValidator:
    @staticmethod
    def is_grade_for_student_and_assignment_existent(grade_list: List, student_id: str, assignment_id: str):
        return bool(
            [grade for grade in grade_list if grade.student_id == student_id and grade.assignment_id == assignment_id]
        )

    @staticmethod
    def is_assignment_for_student_ungraded(grade_list: List, student_id: str, assignment_id: str):
        grade = [
            grade for grade in grade_list if grade.student_id == student_id and grade.assignment_id == assignment_id
        ]

        if not grade:
            raise GradeValidatorException("Grade not found.")

        grade = grade[0]

        return not bool(grade.grade_value)

    @staticmethod
    def validate_grade_unique(grade_list: List, student_id: str, assignment_id: str):
        if GradeValidator.is_grade_for_student_and_assignment_existent(grade_list, student_id, assignment_id):
            raise GradeValidatorException(f"Grade with assignment_id={assignment_id} and"
                                          f" student_id={student_id} already exists.")

    @staticmethod
    def validate_grade_value(grade_value: int):
        if not isinstance(grade_value, int):
            raise GradeValidatorException("Grade value needs to be an integer.")

    @staticmethod
    def validate_grade(
            grade_list: List,
            student_list: List,
            assignment_list: List,
            student_id: str,
            assignment_id: str,
            grade_value: Optional[int] = None
    ):
        if not StudentValidator.is_id_used(student_list, student_id):
            raise GradeValidatorException("Wrong student_id.")
        if not AssignmentValidator.is_id_used(assignment_list, assignment_id):
            raise GradeValidatorException("Wrong assignment_id.")
        GradeValidator.validate_grade_unique(grade_list, student_id, assignment_id)
        if grade_value:
            GradeValidator.validate_grade_value(grade_value)
