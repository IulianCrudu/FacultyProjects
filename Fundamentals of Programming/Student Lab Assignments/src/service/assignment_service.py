from datetime import datetime
from copy import deepcopy

from src.domain import Assignment
from src.validators import AssignmentValidator
from src.service.undo_service import Operation, FunctionCall


class AssignmentServiceException(Exception):
    def __init__(self, msg):
        self._msg = msg


class AssignmentService:
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

    def get_all_assignments(self):
        """
        Returns all the assignments in the repo
        :return: [Assignment]
        """
        return self.repo.items

    @staticmethod
    def get_deadline_from_string(deadline: str):
        # Deadline should have this format: dd-mm-yyyy hh:mm
        date_format = "%d-%m-%Y %H:%M"

        return datetime.strptime(deadline, date_format)

    @staticmethod
    def get_string_from_datetime(deadline: datetime):
        date_format = "%d-%m-%Y %H:%M"

        return deadline.strftime(date_format)

    def add_assignment(self, assignment_id: str, description: str, deadline: str, create_undo=True):
        """
        Adds a new assignment to the repo
        :param assignment_id: The assignment's ID
        :param description: The assignment's description
        :param deadline: The assignment's deadline string
        :param create_undo: If the action should be added to history or not
        :return: None
        """

        AssignmentValidator.validate_assignment(
            assignment_list=self.repo.items,
            assignment_id=assignment_id,
            description=description,
            deadline=deadline
        )

        deadline_obj = AssignmentService.get_deadline_from_string(deadline)

        assignment = Assignment(assignment_id=assignment_id, description=description, deadline=deadline_obj)
        self.repo.add_item(assignment)

        if create_undo:
            undo_func = FunctionCall(self.remove_assignment, assignment_id, create_undo=False)
            redo_func = FunctionCall(self.add_assignment, assignment_id, description, deadline, create_undo=False)
            operation = Operation(undo_func, redo_func)
            self.undo_service.record(operation)

    def remove_assignment(self, assignment_id: str, cascaded_operation=None, create_undo=True):
        """
            Removes an assignment from the repo
            :param assignment_id: The id of the assignment to be removed
            :param cascaded_operation: The cascaded operation that we have to extend—if any
            :param create_undo: If the action should be added to history or not
            :return:
        """
        if not AssignmentValidator.is_id_used(self.repo.items, assignment_id):
            raise AssignmentServiceException("Assignment with given id not found.")

        assignment = self.repo.delete_item(assignment_id)

        if create_undo:
            redo_fun = FunctionCall(self.remove_assignment, assignment_id, create_undo=False)
            undo_fun = FunctionCall(
                self.add_assignment,
                assignment_id,
                assignment.description,
                AssignmentService.get_string_from_datetime(assignment.deadline),
                False
            )
            operation = Operation(undo_fun, redo_fun)
            if cascaded_operation:
                cascaded_operation.add_operations([operation])
                self.undo_service.record(cascaded_operation)
            else:
                self.undo_service.record(operation)

    def update_assignment(self, assignment_id: str, create_undo=True, **kwargs):
        """
        Update's an assignment fields
        :param assignment_id: The assignment to be updated
        :param create_undo: If the action should be added to history or not
        :param kwargs: Every field that needs to be updated. The fields that don't belong to the item are ignored.
        :return: None
        """
        if kwargs.get("deadline", None):
            kwargs["deadline"] = self.get_deadline_from_string(kwargs["deadline"])
        if not AssignmentValidator.is_id_used(self.repo.items, assignment_id):
            raise AssignmentServiceException("Assignment with given id not found.")
        assignment = deepcopy(self.repo.get(assignment_id))

        self.repo.update_item(assignment_id, **kwargs)

        if create_undo:
            redo_fun = FunctionCall(self.update_assignment, assignment_id, create_undo=False, **kwargs)
            undo_kwargs = dict()
            for field in kwargs:
                if field == "deadline":
                    undo_kwargs[field] = AssignmentService.get_string_from_datetime(assignment.deadline)
                else:
                    undo_kwargs[field] = getattr(assignment, field, None)
            print("undo_kwargs", undo_kwargs)
            undo_fun = FunctionCall(self.update_assignment, assignment_id, create_undo=False, **undo_kwargs)
            self.undo_service.record(Operation(undo_fun, redo_fun))
