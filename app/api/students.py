from fastapi import APIRouter, HTTPException, status, Query
from uuid import UUID  
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate
from app.repositories.student_repository import student_repository

router = APIRouter(prefix="/api/v1/students", tags=["students"])

@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate):
    try:
        return student_repository.create(student_in)
    except ValueError as e:
        if str(e) == "Email already exists":
            raise HTTPException(status_code=409, detail="Student with this email already exists")
        raise HTTPException(status_code=422, detail=str(e))

@router.get("", response_model=list[StudentRead])
def get_students(study_program: str | None = Query(None, description="Фільтр за назвою освітньої програми")):
    all_students = student_repository.get_all()
    
    if study_program:
        target_program = study_program.strip().lower()
        return [s for s in all_students if s.get("study_program", "").strip().lower() == target_program]
        
    return all_students

@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: UUID):
    student = student_repository.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.patch("/{student_id}", response_model=StudentRead)
def update_student(student_id: UUID, student_in: StudentUpdate):
    try:
        student = student_repository.update(student_id, student_in)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except ValueError as e:
        if str(e) == "Email already exists":
            raise HTTPException(status_code=409, detail="Email already taken")
        if str(e) == "Empty update body":
            raise HTTPException(status_code=422, detail="At least one field must be provided for update")
        raise HTTPException(status_code=422, detail=str(e))
