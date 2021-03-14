class GradeException(Exception):
    def __init__(self, msg):
        self._msg = msg


class Grade:
    def __init__(self, assignment_id: str, student_id: str, grade_value: int):
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.grade_value = grade_value

    def __str__(self):
        return f"Grade(assignment_id={self.assignment_id}, student_id={self.student_id}," \
               f" grade={self.grade_value or 'Not graded yet.'})"

    @property
    def assignment_id(self):
        return self._assignment_id

    @assignment_id.setter
    def assignment_id(self, value):
        self._assignment_id = value

    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, value):
        self._student_id = value

    @property
    def grade_value(self):
        return self._grade_value

    @grade_value.setter
    def grade_value(self, value):
        self._grade_value = value
