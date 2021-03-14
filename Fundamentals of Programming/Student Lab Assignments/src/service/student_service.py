from copy import deepcopy

from src.domain import Student
from .undo_service import Operation, FunctionCall


class StudentServiceException(Exception):
    def __init__(self, msg):
        self._msg = msg


class StudentService:
    def __init__(self, repo, validator, undo_service):
        self._repo = repo
        self._validator = validator
        self._undo_service = undo_service

    @property
    def repo(self):
        return self._repo

    @property
    def validator(self):
        return self._validator

    @property
    def undo_service(self):
        return self._undo_service

    def get_all_students(self):
        """
        Returns all the students in the repo
        :return: [Student]
        """
        return self.repo.items

    def add_student(self, student_id: str, name: str, group: str, create_undo=True):
        """
        Adds a new student to the repo
        :param student_id: The id of the student
        :param name: The name of the student
        :param group: The group of the student
        :param create_undo: If the action should be added to history or not
        :return: None
        """
        if create_undo:
            undo_fun = FunctionCall(self.remove_student, student_id, create_undo=False)
            redo_fun = FunctionCall(self.add_student, student_id, name, group, False)
            self.undo_service.record(Operation(undo_fun, redo_fun))

        self.validator.validate_student(
            student_list=self.repo.items,
            student_id=student_id,
            name=name,
            group=group
        )
        student = Student(student_id, name, group)
        self.repo.add_item(student)

    def remove_student(self, student_id: str, cascaded_operation=None, create_undo=True):
        """
        Removes a student from the repo
        :param student_id: The id of the student to be removed
        :param cascaded_operation: The cascaded operation that we have to extend—if any
        :param create_undo: If the action should be added to history or not
        :return:
        """
        student = self.repo.get(student_id)
        if create_undo:
            redo_fun = FunctionCall(self.remove_student, student_id, create_undo=False)
            undo_fun = FunctionCall(self.add_student, student_id, student.name, student.group, False)
            operation = Operation(undo_fun, redo_fun)
            if cascaded_operation:
                cascaded_operation.add_operations([operation])
                self.undo_service.record(cascaded_operation)
            else:
                self.undo_service.record(operation)

        if not self.validator.is_id_used(self.repo.items, student_id):
            raise StudentServiceException("Student with given id not found.")

        self.repo.delete_item(student_id)

    def update_student(self, student_id: str, create_undo=True, **kwargs):
        """
        Updates a student's fields
        :param student_id: The student to be updated
        :param create_undo: If the action should be added to history or not
        :param kwargs: Every field that needs to be updated. The fields that don't belong to the item are ignored.
        :return: None
        """
        if not self.validator.is_id_used(self.repo.items, student_id):
            raise StudentServiceException("Student with given id not found.")
        student = deepcopy(self.repo.get(student_id))

        self.repo.update_item(student_id, **kwargs)

        if create_undo:
            redo_fun = FunctionCall(self.update_student, student_id, create_undo=False, **kwargs)
            undo_kwargs = dict()
            for field in kwargs:
                undo_kwargs[field] = getattr(student, field, None)
            undo_fun = FunctionCall(self.update_student, student_id, create_undo=False, **undo_kwargs)
            self.undo_service.record(Operation(undo_fun, redo_fun))
