import uuid
from uuid import UUID
from app.schemas.student import StudentCreate, StudentUpdate

class StudentRepository:
    def __init__(self):
        self._storage = {}

    def create(self, student_in: StudentCreate) -> dict:
        for student in self._storage.values():
            if student["email"].lower() == student_in.email.lower():
                raise ValueError("Email already exists")

        student_id = uuid.uuid4()
        
        new_student = {
            "id": student_id,
            **student_in.model_dump() 
        }
        
        self._storage[student_id] = new_student
        return new_student

    def get_all(self) -> list[dict]:
        return list(self._storage.values())

    def get_by_id(self, student_id: UUID) -> dict | None:
        return self._storage.get(student_id)

    def update(self, student_id: UUID, student_in: StudentUpdate) -> dict | None:
        if student_id not in self._storage:
            return None

        update_data = student_in.model_dump(exclude_unset=True)
        
        if not update_data:
            raise ValueError("Empty update body")

        if "email" in update_data:
            new_email = update_data["email"].lower()
            for k, student in self._storage.items():
                if k != student_id and student["email"].lower() == new_email:
                    raise ValueError("Email already exists")

        current_student = self._storage[student_id]
        current_student.update(update_data)
        return current_student

student_repository = StudentRepository()
