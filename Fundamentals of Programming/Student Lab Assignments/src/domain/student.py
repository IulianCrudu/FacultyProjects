from typing import Union
from uuid import UUID


class StudentException(Exception):
    def __init__(self, msg):
        self._msg = msg


class Student:
    def __init__(self, student_id: Union[str, UUID], name: str, group: str):
        self.student_id = student_id
        self.name = name
        self.group = group

    def __str__(self):
        return f"Student(id={self.student_id}, name={self.name}, group={self.group})"

    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, value):
        self._student_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value
