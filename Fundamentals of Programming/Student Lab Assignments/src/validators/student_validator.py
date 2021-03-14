from typing import List


class StudentValidatorException(Exception):
    def __init__(self, msg):
        self._msg = msg


class StudentValidator:
    @staticmethod
    def is_id_used(student_list: List, student_id: str):
        return bool([student for student in student_list if student.student_id == student_id])

    @staticmethod
    def validate_id_unique(student_list: List, student_id: str):
        if StudentValidator.is_id_used(student_list, student_id):
            raise StudentValidatorException(f"Student with id={student_id} exists.")

    @staticmethod
    def validate_student_id(student_list: List, student_id: str):
        if not isinstance(student_id, str):
            raise StudentValidatorException("Student's ID must be a string.")
        StudentValidator.validate_id_unique(student_list, student_id)

    @staticmethod
    def validate_name(name: str):
        if not isinstance(name, str):
            raise StudentValidatorException("Student's name must be a string.")

    @staticmethod
    def validate_group(group: str):
        if not isinstance(group, str):
            raise StudentValidatorException("Student's group must be a string.")

    @staticmethod
    def is_group_used(student_list: List, group: str):
        return bool([student for student in student_list if student.group == group])

    @staticmethod
    def validate_student(student_list: List, student_id: str, name: str, group: str):
        StudentValidator.validate_student_id(student_list, student_id)
        StudentValidator.validate_name(name)
        StudentValidator.validate_group(group)
