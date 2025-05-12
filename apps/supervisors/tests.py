import pytest
from django.utils import timezone
from datetime import datetime
from apps.internships.models import Internship, InternshipRequest

@pytest.mark.django_db
def test_supervisor_internship_requests(client, supervisor_user, student_user, company, academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/supervisors/requests/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['job_description'] == "Test internship"

@pytest.mark.django_db
def test_approve_internship_request(client, supervisor_user, student_user, company, academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 200
    assert response.data['message'] == "Internship request approved and internship created."
    assert Internship.objects.count() == 1
    internship = Internship.objects.first()
    assert internship.lecturer is None
    internship_request.refresh_from_db()
    assert internship_request.status == "approved"

@pytest.mark.django_db
def test_approve_internship_request_wrong_role(client, student_user, company, academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "student@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 403
    assert response.data['error'] == "Only supervisors can approve internship requests."

@pytest.mark.django_db
def test_approve_internship_request_unapproved_supervisor(client, unapproved_supervisor_user, student_user, company, academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "unapproved@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 403
    assert response.data['error'] == "Only approved supervisors can approve requests."

@pytest.mark.django_db
def test_approve_internship_request_wrong_company(client, supervisor_user, student_user, other_company, academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=other_company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.post(f'/api/supervisors/requests/approve/{internship_request.id}/')
    assert response.status_code == 403
    assert response.data['error'] == "This request does not belong to your company."