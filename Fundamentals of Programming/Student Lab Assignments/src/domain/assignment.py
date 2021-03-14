from datetime import datetime


class AssignmentException(Exception):
    def __init__(self, msg):
        self._msg = msg


class Assignment:
    def __init__(self, assignment_id: str, description: str, deadline: datetime):
        self.assignment_id = assignment_id
        self.description = description
        self.deadline = deadline

    def __str__(self):
        return f"Assignment(assignment_id={self.assignment_id}," \
               f" description={self.description}, deadline={self.deadline})"

    @property
    def assignment_id(self):
        return self._assignment_id

    @assignment_id.setter
    def assignment_id(self, value):
        self._assignment_id = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        self._deadline = value
