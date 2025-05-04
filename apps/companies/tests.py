import pytest
from rest_framework.test import APIClient
from apps.companies.models import CompanyAdmin
from apps.internships.models import Internship, InternshipRequest
from apps.supervisors.models import Supervisor
from apps.users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def company_admin_user(company):
    user = User.objects.create_user(
        email="admin@techcorp.com", password="password123",
        full_name="Company Admin", contact="+237623456789", role="company_admin"
    )
    return CompanyAdmin.objects.create(user=user, company=company)


@pytest.fixture
def supervisor_user(company):
    user = User.objects.create_user(
        email="supervisor@techcorp.com", password="password123",
        full_name="Supervisor User", contact="+237623456789", role="supervisor"
    )
    return Supervisor.objects.create(user=user, company=company)


@pytest.mark.django_db
def test_company_admin_internship_requests(client, company_admin_user, student_user, company, academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/companies/admins/requests/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['job_description'] == "Test internship"


@pytest.mark.django_db
def test_approve_internship_request(client, company_admin_user, supervisor_user, student_user, company, academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {"supervisor_id": str(supervisor_user.id)}
    response = client.post(f'/api/companies/admins/requests/approve/{internship_request.id}/', payload)
    assert response.status_code == 200
    assert response.data['job_description'] == "Test internship"
    assert response.data['status'] == "waiting"  # Since start_date is future
    assert Internship.objects.count() == 1
    internship_request.refresh_from_db()
    assert internship_request.status == "approved"


@pytest.mark.django_db
def test_approve_internship_request_wrong_role(client, supervisor_user, student_user, company, academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {"supervisor_id": str(supervisor_user.id)}
    response = client.post(f'/api/companies/admins/requests/approve/{internship_request.id}/', payload)
    assert response.status_code == 403
    assert response.data['error'] == "Only company admins can approve internship requests."
