import pytest
from rest_framework.test import APIClient

from apps.companies.models import Company
from apps.supervisors.models import Supervisor
from apps.internships.models import InternshipRequest
from apps.internships.models import Internship
from apps.users.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def supervisor_user(company):
    user = User.objects.create_user(
        email="supervisor@techcorp.com", password="password123",
        full_name="Supervisor User", contact="+237623456789", role="supervisor"
    )
    return Supervisor.objects.create(user=user, company=company, status="approved")


@pytest.fixture
def unapproved_supervisor_user(company):
    user = User.objects.create_user(
        email="unapproved@techcorp.com", password="password123",
        full_name="Unapproved Supervisor", contact="+237623456789", role="supervisor"
    )
    return Supervisor.objects.create(user=user, company=company, status="pending")


@pytest.fixture
def other_company():
    return Company.objects.create(
        name="Other Corp", address="456 Street", contact="+237623456789",
        email="contact@othercorp.com", division="HR", designation="Manager"
    )


@pytest.mark.django_db
def test_supervisor_internship_requests(client, supervisor_user, student_user, company, academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/users/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/supervisors/requests/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['job_description'] == "Test internship"


@pytest.mark.django_db
def test_approve_internship_request(client, supervisor_user, student_user, company, academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/users/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 200
    assert response.data['message'] == "Internship request approved and internship created."
    assert Internship.objects.count() == 1
    internship = Internship.objects.first()
    assert internship.lecturer is None  # No lecturer assigned
    internship_request.refresh_from_db()
    assert internship_request.status == "approved"


@pytest.mark.django_db
def test_approve_internship_request_wrong_role(client, student_user, company, academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/users/login/', {"email": "student@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 403
    assert response.data['error'] == "Only supervisors can approve internship requests."


@pytest.mark.django_db
def test_approve_internship_request_unapproved_supervisor(client, unapproved_supervisor_user, student_user, company,
                                                          academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/users/login/', {"email": "unapproved@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 403
    assert response.data['error'] == "Only approved supervisors can approve requests."


@pytest.mark.django_db
def test_approve_internship_request_wrong_company(client, supervisor_user, student_user, other_company, academic_year):
    internship_request = InternshipRequest.objects.create(
        student=student_user, company=other_company, academic_year=academic_year,
        start_date="2025-06-01", end_date="2025-08-01", job_description="Test internship"
    )
    response = client.post('/api/users/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 403
    assert response.data['error'] == "This request does not belong to your company."