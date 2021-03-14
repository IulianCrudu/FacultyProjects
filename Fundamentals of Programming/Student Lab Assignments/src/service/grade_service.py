from typing import Optional
from datetime import datetime

from src.domain import Grade
from src.service.undo_service import CascadedOperation, FunctionCall, Operation


class GradeServiceException(Exception):
    def __init__(self, msg):
        self._msg = msg


class GradeService:
    def __init__(self, grade_repo, student_repo, assignment_repo, validator, undo_service):
        self._repo = grade_repo
        self._student_repo = student_repo
        self._assignment_repo = assignment_repo
        self._validator = validator
        self._undo_service = undo_service

    @property
    def repo(self):
        return self._repo

    @property
    def student_repo(self):
        return self._student_repo

    @property
    def assignment_repo(self):
        return self._assignment_repo

    @property
    def validator(self):
        return self._validator

    @property
    def undo_service(self):
        return self._undo_service

    def get_all_grades(self):
        """
        Returns all the grade from the repo
        :return: All the grades in the repo
        """
        return self.repo.items

    def add_grade(self, assignment_id: str, student_id: str, grade_value: Optional[int] = None, create_undo=True):
        """
        Adds a new grade to the repo
        :param assignment_id: The assignment for the grade
        :param student_id: The grade's student
        :param grade_value: The value of the grade
        :param create_undo: If the action should be added to history or not
        :return:
        """
        self.validator.validate_grade(
            grade_list=self.repo.items,
            student_list=self.student_repo.items,
            assignment_list=self.assignment_repo.items,
            student_id=student_id,
            assignment_id=assignment_id,
            grade_value=grade_value
        )

        grade = Grade(assignment_id, student_id, grade_value)
        self.repo.add_item(grade)
        if create_undo:
            undo_func = FunctionCall(self.remove_grade, student_id, assignment_id)
            redo_func = FunctionCall(self.add_grade, assignment_id, student_id, grade_value, create_undo=False)
            self.undo_service.record(Operation(undo_func, redo_func))

        return grade

    def student_has_assignment(self, assigment_id: str, student_id: str):
        return bool([
            grade for grade in self.repo.items
            if grade.assignment_id == assigment_id and grade.student_id == student_id
        ])

    def give_assignment_to_group(self, assignment_id: str, group: str, create_undo=True):
        added_grades = []
        for student in self.student_repo.items:
            if student.group != group:
                continue
            if self.student_has_assignment(assignment_id, student.student_id):
                continue

            grade = self.add_grade(assignment_id, student.student_id)
            added_grades.append(grade)

        if create_undo:
            undo_func = FunctionCall(self.remove_grade_for_assignment_and_group, assignment_id, group)
            redo_func = FunctionCall(self.give_assignment_to_group, assignment_id, group, create_undo=False)
            self.undo_service.record(Operation(undo_func, redo_func))

    def get_sorted_students_for_assignment(self, assignment_id: str):
        students_dict = [
            {
                "student": self.student_repo.get(grade.student_id),
                "grade": grade.grade_value
            } for grade in self.repo.get(assignment_id=assignment_id)
        ]
        students_dict.sort(key=lambda student: student["grade"] or 0, reverse=True)
        return students_dict

    def get_ungraded_assignments_for_student(self, student_id: str):
        assignment_ids = [
            grade.assignment_id for grade in self.repo.get(student_id=student_id) if not grade.grade_value
        ]

        return [self.assignment_repo.get(assignment_id) for assignment_id in assignment_ids]

    def _get_expired_assignments(self):
        now = datetime.now()
        return [assignment for assignment in self.assignment_repo.items if now > assignment.deadline]

    def get_late_students(self):
        expired_assignments = self._get_expired_assignments()
        late_student_ids = set()
        for assignment in expired_assignments:
            assignment_grades = self.repo.get(assignment_id=assignment.assignment_id)
            late_student_ids.update([grade.student_id for grade in assignment_grades])
        return [self.student_repo.get(student_id) for student_id in late_student_ids]

    def get_sorted_students_by_avg_grade(self):
        students_dict = []
        for student in self.student_repo.items:
            grades = self.repo.get(student_id=student.student_id)
            grade_sum = 0
            grade_nr = 0
            for grade in grades:
                if grade.grade_value:
                    grade_sum += grade.grade_value
                    grade_nr += 1
            if grade_nr:
                students_dict.append(dict(student=student, avg_grade=grade_sum/grade_nr))
        students_dict.sort(key=lambda student_dict: student_dict['avg_grade'], reverse=True)
        return students_dict

    def grade_assignment_for_student(
            self,
            student_id: str,
            assignment_id: str,
            grade_value: Optional[int] = None,
            create_undo=True
    ):
        old_grade_value = self.repo.get(student_id=student_id, assignment_id=assignment_id).grade_value
        self.repo.update_grade(student_id, assignment_id, grade_value)

        if create_undo:
            undo_func = FunctionCall(
                self.grade_assignment_for_student,
                student_id,
                assignment_id,
                old_grade_value,
                create_undo=False
            )
            redo_func = FunctionCall(
                self.grade_assignment_for_student,
                student_id,
                assignment_id,
                grade_value,
                create_undo=False
            )
            self.undo_service.record(Operation(undo_func, redo_func))

    def remove_grades_for_student(self, student_id: str, create_undo=True):
        deleted_items = self.repo.delete_grades(student_id=student_id)

        if create_undo:
            redo_func = FunctionCall(self.remove_grades_for_student, student_id, create_undo=False)
            undo_func = FunctionCall(self.repo.add_items, *deleted_items)
            operation = Operation(undo_func, redo_func)
            return CascadedOperation(operation)

    def remove_grades_for_assignment(self, assignment_id: str, create_undo=True):
        deleted_items = self.repo.delete_grades(assignment_id=assignment_id)

        if create_undo:
            redo_func = FunctionCall(self.remove_grades_for_assignment, assignment_id, create_undo=False)
            undo_func = FunctionCall(self.repo.add_items, *deleted_items)
            operation = Operation(undo_func, redo_func)
            return CascadedOperation(operation)

    def remove_grade_for_assignment_and_group(self, assignment_id: str, group: str):
        for student in self.student_repo.items:
            if student.group == group:
                self.remove_grade(student.student_id, assignment_id)

    def remove_grade(self, student_id: str, assignment_id: str):
        return self.repo.delete_grades(student_id=student_id, assignment_id=assignment_id)
