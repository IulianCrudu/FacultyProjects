from src.ui.menu_ui import UI
from src.service import StudentService, AssignmentService, GradeService, UndoService
from src.repository import Repository, GradeRepository
from src.validators import StudentValidator, AssignmentValidator, GradeValidator

undo_service = UndoService()

student_repository = Repository(pk="student_id")
student_service = StudentService(repo=student_repository, validator=StudentValidator, undo_service=undo_service)

assignment_repository = Repository(pk="assignment_id")
assignment_service = AssignmentService(
    repo=assignment_repository,
    validator=AssignmentValidator,
    undo_service=undo_service
)

grade_repository = GradeRepository()
grade_service = GradeService(
    grade_repo=grade_repository,
    assignment_repo=assignment_repository,
    student_repo=student_repository,
    validator=GradeValidator,
    undo_service=undo_service
)

cli_ui = UI(
    student_service=student_service,
    assignment_service=assignment_service,
    grade_service=grade_service,
    undo_service=undo_service
)
cli_ui.start()
