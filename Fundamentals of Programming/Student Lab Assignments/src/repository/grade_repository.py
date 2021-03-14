from typing import Optional

from .repository import RepositoryException


class GradeRepository:
    def __init__(self):
        self._items = []

    def get(self, student_id: Optional[str] = None, assignment_id: Optional[str] = None):
        """
        Returns the item from the list for the given student_id and assignment_id
        :param student_id: The student id of the grade
        :param assignment_id: The assignment_id of the grade
        :return: The found item/items
        :raises:
            RepositoryException - if there is no item with that student_id and assignment_id
        """
        if not assignment_id and not student_id:
            raise RepositoryException("At least one student_id or assignment_id should be given.")

        if not assignment_id:
            return [grade for grade in self.items if grade.student_id == student_id]

        if not student_id:
            return [grade for grade in self.items if grade.assignment_id == assignment_id]

        found_grade = [
            grade for grade in self.items
            if grade.assignment_id == assignment_id and grade.student_id == student_id
        ]

        if not found_grade:
            raise RepositoryException(f"Grade(student_id={student_id}, assignment_id={assignment_id}) not found.")

        return found_grade[0]

    def __len__(self):
        return len(self.items)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    def add_item(self, item):
        """
        Adds a new item to the listX
        :param item: The item to be added
        :return: None
        """
        self.items.append(item)

    def add_items(self, *items):
        self.items.extend(items)

    def update_grade(self, student_id: str, assignment_id: str, new_grade_value: int):
        """
        Updates the grade_value for a certain grade
        :param student_id: The student_id of the grade
        :param assignment_id: The assignment_id of the grade
        :param new_grade_value: The new grade_value of the grade
        :return: None
        """
        grade = self.get(student_id=student_id, assignment_id=assignment_id)
        # if grade.grade_value:
        #     raise RepositoryException("Can't update a grade's value.")
        grade.grade_value = new_grade_value

    def delete_grades(self, student_id: Optional[str] = None, assignment_id: Optional[str] = None):
        """
        Deletes the grade for a certain student_id and/or assignment_id
        :param student_id: The student_id of the grade(s)
        :param assignment_id: The assignment_id of the grade(s)
        :return: None
        """
        if not assignment_id and not student_id:
            raise RepositoryException("At least one student_id or assignment_id should be given.")

        if not assignment_id:
            deleted_items = [grade for grade in self.items if grade.student_id == student_id]
            self.items = [grade for grade in self.items if grade.student_id != student_id]
            return deleted_items

        if not student_id:
            deleted_items = [grade for grade in self.items if grade.assignment_id == assignment_id]
            self.items = [grade for grade in self.items if grade.assignment_id != assignment_id]
            return deleted_items

        deleted_items = [
            grade for grade in self.items
            if grade.assignment_id == assignment_id and grade.student_id == student_id
        ]

        self.items = [
            grade for grade in self.items
            if not (grade.assignment_id == assignment_id and grade.student_id == student_id)
        ]

        return deleted_items
