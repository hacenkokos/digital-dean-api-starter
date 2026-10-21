from pydantic import BaseModel, ConfigDict, Field, EmailStr
from uuid import UUID

class StrictModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",             
        str_strip_whitespace=True   
    )

class StudentCreate(StrictModel):
    full_name: str = Field(..., min_length=5, max_length=120)
    
    email: EmailStr
    
    group_code: str = Field(..., pattern=r"^[A-ZА-ЯІЄЇҐa-zа-яієїїґ]{2,4}-\d{2}$")
    study_program: str = Field(..., min_length=2, max_length=100)

class StudentUpdate(StrictModel):
    full_name: str | None = Field(None, min_length=5, max_length=120)
    email: EmailStr | None = None
    group_code: str | None = Field(None, pattern=r"^[A-ZА-ЯІЄЇҐa-zа-яієїїґ]{2,4}-\d{2}$")
    study_program: str | None = Field(None, min_length=2, max_length=100)

class StudentRead(StrictModel):
    id: UUID
    full_name: str
    email: str
    group_code: str
    study_program: str
