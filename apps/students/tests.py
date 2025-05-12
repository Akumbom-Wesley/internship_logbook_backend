import pytest

from django.utils import timezone
from datetime import datetime

from apps.users.models import User
from apps.internships.models import InternshipRequest

@pytest.mark.django_db
def test_list_students(client, student_user):
    user = User.objects.create_user(
        email="admin@example.com", password="password123",
        full_name="Admin User", contact="+237623456789", role="super_admin", is_staff=True
    )
    response = client.post('/api/auth/login/', {"email": "admin@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/students/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['matricule_num'] == "UBa25E0001"

@pytest.mark.django_db
def test_create_internship_request(client, student_user, company, academic_year):
    response = client.post('/api/auth/login/', {"email": "student@example.com", "password": "password123"})
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
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "student@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/students/requests/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['job_description'] == "Test internship"
    assert response.data[0]['student'] == "Student User - UBa25E0001"
    assert response.data[0]['company'] == "Tech Corp"