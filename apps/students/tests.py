from django.test import TestCase

# Create your tests here.
import pytest
from rest_framework.test import APIClient
from apps.students.models import Student
from apps.departments.models import Department, School
from apps.companies.models import Company
from apps.academic_years.models import AcademicYear
from apps.users.models import User
from apps.internships.models import InternshipRequest


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def school():
    return School.objects.create(name="Science")


@pytest.fixture
def department(school):
    return Department.objects.create(name="Computer Science", school=school)


@pytest.fixture
def company():
    return Company.objects.create(
        name="Tech Corp", address="123 Street", contact="+237623456789",
        email="contact@techcorp.com", division="IT", designation="Manager"
    )


@pytest.fixture
def academic_year():
    return AcademicYear.objects.create(start_year=2024, end_year=2025)


@pytest.fixture
def student_user(department):
    user = User.objects.create_user(
        email="student@example.com", password="password123",
        full_name="Student User", contact="+237623456789", role="student"
    )
    return Student.objects.create(user=user, matricule_num="UBa25E0001", department=department)


@pytest.mark.django_db
def test_list_students(client, student_user):
    user = User.objects.create_user(
        email="admin@example.com", password="password123",
        full_name="Admin User", contact="+237623456789", role="super_admin", is_staff=True
    )
    response = client.post('/api/users/login/', {"email": "admin@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/students/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['matricule_num'] == "UBa25E0001"


@pytest.mark.django_db
def test_create_internship_request(client, student_user, company, academic_year):
    response = client.post('/api/users/login/', {"email": "student@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {
        "company": str(company.id),
        "academic_year": str(academic_year.id),
        "start_date": "2025-06-01T00:00:00Z",
        "end_date": "2025-08-01T00:00:00Z",
        "job_description": "Software development internship"
    }
    response = client.post('/api/students/requests/create/', payload)
    assert response.status_code == 201
    assert response.data['status'] == "pending"
    assert response.data['student'] == "Student User - UBa25E0001"
    assert response.data['company'] == "Tech Corp"
    assert InternshipRequest.objects.count() == 1


@pytest.mark.django_db
def test_student_internship_requests(client, student_user, company, academic_year):
    InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/users/login/', {"email": "student@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/students/requests/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['job_description'] == "Test internship"
    assert response.data[0]['student'] == "Student User - UBa25E0001"
    assert response.data[0]['company'] == "Tech Corp"