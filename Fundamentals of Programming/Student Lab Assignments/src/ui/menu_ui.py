from src.tests.test_student import TestStudent
from src.tests.test_assignment import TestAssignment
from src.tests.test_grade import TestGrade
from src.repository import RepositoryException
from src.validators import (
    StudentValidator,
    StudentValidatorException,
    AssignmentValidator,
    AssignmentValidatorException,
    GradeValidator,
    GradeValidatorException
)
from src.service.student_service import StudentServiceException
from src.service.assignment_service import AssignmentServiceException


class UI:
    def __init__(self, student_service, assignment_service, grade_service, undo_service):
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service
        self._undo_service = undo_service

    @property
    def student_service(self):
        return self._student_service

    @property
    def assignment_service(self):
        return self._assignment_service

    @property
    def grade_service(self):
        return self._grade_service

    @property
    def undo_service(self):
        return self._undo_service

    @staticmethod
    def print_menu():
        print("1.0 List students")
        print("1.1 Add a student")
        print("1.2 Update a student")
        print("1.3 Remove a student")
        print("--------------------")
        print("2.0 List assignments")
        print("2.1 Add an assignment")
        print("2.2 Update an assignment")
        print("2.3 Remove an assignment")
        print("--------------------")
        print("3.0 List grades")
        print("3.1 Give assignment to a student")
        print("3.2 Give assignment to a group")
        print("3.3 Grade assignment for student")
        print("--------------------")
        print("4.1 All students who received a given assignment, ordered by average grade for that assignment.")
        print("4.2 All students who are late with at least one assignment.")
        print("4.3 Students with the best school situation.")
        print("--------------------")
        print("5.1 Undo last operation")
        print("5.2 Redo last operation")

    #  ---------------- Student ----------------
    def list_students_ui(self):
        students = self.student_service.get_all_students()
        for index, student in enumerate(students):
            print(f"{index}. {student}")
        print("\n")

    def add_student_ui(self):
        student_id = input("Enter the student's id: ")
        name = input("Enter the student's name: ")
        group = input("Enter the student's group: ")
        self.student_service.add_student(student_id, name, group)

    def remove_student_ui(self):
        student_id = input("Enter the student's id: ")
        if not StudentValidator.is_id_used(self.student_service.get_all_students(), student_id):
            print("The given id isn't used.")
            return
        cascaded_operation = self.grade_service.remove_grades_for_student(student_id)
        self.student_service.remove_student(student_id, cascaded_operation=cascaded_operation)

    def update_student_ui(self):
        student_id = input("Enter the student's id: ")
        new_name = input("Update the student's name. Leave empty if not needed.: ")
        new_group = input("Update the student's group. Leave empty if not needed.: ")

        if not new_group and not new_name:
            print("At least one field needs to be updated.")
            return

        update_fields = dict()
        if new_group:
            update_fields["group"] = new_group
        if new_name:
            update_fields["name"] = new_name
        if not StudentValidator.is_id_used(self.student_service.get_all_students(), student_id):
            print("The given id isn't used.")
            return
        self.student_service.update_student(student_id, **update_fields)

    # ---------------- Assignment ----------------
    def list_assignments_ui(self):
        assignments = self.assignment_service.get_all_assignments()
        for index, assignment in enumerate(assignments):
            print(f"{index}. {assignment}")
        print("\n")

    def add_assignment_ui(self):
        assignment_id = input("Enter the assignment's id: ")
        description = input("Enter the assignment's description: ")
        deadline = input("Enter the assignment's deadline in the format of dd-mm-yyyy hh:mm —— ")
        self.assignment_service.add_assignment(assignment_id, description, deadline)

    def remove_assignment_ui(self):
        assignment_id = input("Enter the assignment's id: ")
        if not AssignmentValidator.is_id_used(self.assignment_service.get_all_assignments(), assignment_id):
            print("The given id isn't used.")
            return
        cascaded_operation = self.grade_service.remove_grades_for_assignment(assignment_id)
        self.assignment_service.remove_assignment(assignment_id, cascaded_operation=cascaded_operation)

    def update_assignment_ui(self):
        assignment_id = input("Enter the assignment's id: ")
        new_description = input("Update the assignment's description. Leave empty if not needed.: ")
        new_deadline = input("Update the deadline's group. Leave empty if not needed.: ")

        if not new_description and not new_deadline:
            print("At least one field needs to be updated.")
            return

        update_fields = dict()
        if new_description:
            update_fields["description"] = new_description
        if new_deadline:
            update_fields["deadline"] = new_deadline
        if not AssignmentValidator.is_id_used(self.assignment_service.get_all_assignments(), assignment_id):
            print("The given id isn't used.")
            return
        self.assignment_service.update_assignment(assignment_id, **update_fields)

    # ---------------- Grade ----------------
    def list_grades_ui(self):
        grades = self.grade_service.get_all_grades()
        for index, grade in enumerate(grades):
            print(f"{index}. {grade}")
        print("\n")

    def give_assignment_to_student_ui(self):
        assignment_id = input("Enter assignment's id: ")
        student_id = input("Enter student's id: ")

        if not AssignmentValidator.is_id_used(self.assignment_service.get_all_assignments(), assignment_id):
            print("The given assignment id isn't used.")
            return
        if not StudentValidator.is_id_used(self.student_service.get_all_students(), student_id):
            print("The given student id isn't used.")
            return

        self.grade_service.add_grade(assignment_id=assignment_id, student_id=student_id)

    def give_assignment_to_group_ui(self):
        assignment_id = input("Enter assignment's id: ")
        group = input("Enter group: ")
        group = group.strip()

        if not AssignmentValidator.is_id_used(self.assignment_service.get_all_assignments(), assignment_id):
            print("The given assignment id isn't used.")
            return

        if not StudentValidator.is_group_used(self.student_service.get_all_students(), group):
            print("There's no student in that group. ")
            return

        self.grade_service.give_assignment_to_group(assignment_id=assignment_id, group=group)

    def grade_assignment_to_student_ui(self):
        student_id = input("Enter student's id: ")

        if not StudentValidator.is_id_used(self.student_service.get_all_students(), student_id):
            print("The given student id isn't used.")
            return

        ungraded_assignments = self.grade_service.get_ungraded_assignments_for_student(student_id)

        if ungraded_assignments:
            print("The ungraded assignments for this students are: ")
            for index, grade in enumerate(ungraded_assignments):
                print(f"{index}. {grade}")
        else:
            print("No ungraded assignments for this student")
            return

        assignment_id = input("Enter assignment's id: ")

        if not AssignmentValidator.is_id_used(self.assignment_service.get_all_assignments(), assignment_id):
            print("The given assignment id isn't used.")
            return

        if not GradeValidator.is_assignment_for_student_ungraded(
                self.grade_service.get_all_grades(), student_id, assignment_id
        ):
            print("The given assignment is already graded.")
            return

        grade_value = input("Enter the grade for the assignment: ")

        grade = int(grade_value)

        if grade < 0 or grade > 10:
            print("Invalid grade for the assignment")
            return

        self.grade_service.grade_assignment_for_student(
            student_id=student_id,
            assignment_id=assignment_id,
            grade_value=grade
        )

    # ---------------- Statistics ----------------
    def all_students_who_received_an_assignment_ui(self):
        assignment_id = input("Enter the assignment's id: ")

        if not AssignmentValidator.is_id_used(self.assignment_service.get_all_assignments(), assignment_id):
            print("The given assignment id isn't used.")
            return

        students = self.grade_service.get_sorted_students_for_assignment(assignment_id)
        for index, student_dict in enumerate(students):
            student_grade = student_dict["grade"] or "Not graded yet"
            print(f"{index}. {student_dict['student']} — {student_grade}")
        print("\n")

    def all_students_who_are_late_ui(self):
        students = self.grade_service.get_late_students()
        if not students:
            print("There are no late students")
            return

        for index, student in enumerate(students):
            print(f"{index}. {student}")
        print("\n")

    def students_school_situation_ui(self):
        sorted_students_dict = self.grade_service.get_sorted_students_by_avg_grade()

        if not sorted_students_dict:
            print("There are no students with grades.")
            return

        for index, student_dict in enumerate(sorted_students_dict):
            print(f"{index}. {student_dict['student']} — {student_dict['avg_grade']}")
        print("\n")

    # ---------------- Undo/Redo ----------------
    def undo_operation_ui(self):
        if self.undo_service._index == -1:
            print("Nothing to undo")

        self.undo_service.undo()

    def redo_operation_ui(self):
        res = self.undo_service.redo()
        if not res:
            print("Nothing to redo")

    # ---------------------------------------
    def start(self):
        TestStudent.load_fixtures(self.student_service.repo)
        TestAssignment.load_fixtures(self.assignment_service.repo)
        TestGrade.load_fixtures(
            grade_repo=self.grade_service.repo,
            student_repo=self.student_service.repo,
            assignment_repo=self.assignment_service.repo,
        )
        done = False
        command_dict = {
            "1.0": self.list_students_ui,
            "1.1": self.add_student_ui,
            "1.2": self.update_student_ui,
            "1.3": self.remove_student_ui,
            "2.0": self.list_assignments_ui,
            "2.1": self.add_assignment_ui,
            "2.2": self.update_assignment_ui,
            "2.3": self.remove_assignment_ui,
            "3.0": self.list_grades_ui,
            "3.1": self.give_assignment_to_student_ui,
            "3.2": self.give_assignment_to_group_ui,
            "3.3": self.grade_assignment_to_student_ui,
            "4.1": self.all_students_who_received_an_assignment_ui,
            "4.2": self.all_students_who_are_late_ui,
            "4.3": self.students_school_situation_ui,
            "5.1": self.undo_operation_ui,
            "5.2": self.redo_operation_ui,
        }
        while not done:
            UI.print_menu()
            command = input("Enter the command: ")
            try:
                if command in command_dict:
                    command_dict[command]()
                elif command == '0':
                    print("Exiting...")
                    done = True
                else:
                    print("Bad command entered\n")
            except RepositoryException as re:
                print(f"Repository Error: {str(re)} \n")
            except StudentValidatorException as sve:
                print(f"Student Validation Error: {str(sve)} \n")
            except AssignmentValidatorException as ave:
                print(f"Assignment Validation Error: {str(ave)} \n")
            except StudentServiceException as sse:
                print(f"Student Service Error: {str(sse)} \n")
            except AssignmentServiceException as ase:
                print(f"Assignment Service Error: {str(ase)} \n")
            except GradeValidatorException as gve:
                print(f"Grade Validation Error: {str(gve)} \n")
            except Exception as ve:
                print(str(ve) + "\n")
