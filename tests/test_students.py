import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.repositories.student_repository import student_repository

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_repository():
    student_repository._storage.clear()

def test_create_student_success():
    payload = {
        "full_name": "Іван Петренко",
        "email": "ivan.petrenko@example.com",
        "group_code": "КН-31",
        "study_program": "Комп'ютерні науки"  
    }
    response = client.post("/api/v1/students", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["full_name"] == "Іван Петренко"
    assert data["study_program"] == "Комп'ютерні науки"

def test_create_student_invalid_email():
    payload = {
        "full_name": "Іван Петренко",
        "email": "це-не-email-адреса",
        "group_code": "КН-31"
    }
    response = client.post("/api/v1/students", json=payload)
    assert response.status_code == 422  

def test_patch_student_forbid_extra_field():
    create_resp = client.post("/api/v1/students", json={
        "full_name": "Іван Петренко",
        "email": "ivan@example.com",
        "group_code": "КН-31",
        "study_program": "Комп'ютерні науки"  
    })
    
    assert create_resp.status_code == 201
    student_id = create_resp.json()["id"]
    patch_payload = {
        "group_code": "КН-32",
        "is_admin": True
    }
    response = client.patch(f"/api/v1/students/{student_id}", json=patch_payload)
    assert response.status_code == 422

def test_create_student_with_study_program_success():
    payload = {
        "full_name": "Микола Романюк",
        "email": "mykola.romanyuk@example.com",
        "group_code": "КН-31",
        "study_program": "Інженерія програмного забезпечення" 
    }
    response = client.post("/api/v1/students", json=payload)
    assert response.status_code == 201
    assert response.json()["study_program"] == "Інженерія програмного забезпечення"

def test_create_student_with_study_program_too_short():
    payload = {
        "full_name": "Микола Романюк",
        "email": "mykola.romanyuk@example.com",
        "group_code": "КН-31",
        "study_program": "А" 
    }
    response = client.post("/api/v1/students", json=payload)
    assert response.status_code == 422 

def test_get_students_filtering_by_program():
    client.post("/api/v1/students", json={
        "full_name": "Студент Один",
        "email": "one@example.com",
        "group_code": "КН-31",
        "study_program": "Комп'ютерні науки"
    })
    client.post("/api/v1/students", json={
        "full_name": "Студент Два",
        "email": "two@example.com",
        "group_code": "КН-31",
        "study_program": "Кібербезпека"
    })

    response = client.get("/api/v1/students?study_program=Кібербезпека")
    assert response.status_code == 200
    results = response.json()
    
    assert len(results) == 1
    assert results[0]["full_name"] == "Студент Два"

