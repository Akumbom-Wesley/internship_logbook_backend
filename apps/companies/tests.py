import pytest
from django.utils import timezone
from datetime import datetime
from apps.internships.models import Internship, InternshipRequest

@pytest.mark.django_db
def test_company_admin_internship_requests(client, company_admin_user, student_user, company, academic_year):

    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
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
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {"supervisor_id": str(supervisor_user.id)}
    response = client.post(f'/api/companies/admins/requests/approve/{internship_request.id}/', payload)
    assert response.status_code == 200
    assert response.data['job_description'] == "Test internship"
    assert response.data['status'] == "waiting"
    assert Internship.objects.count() == 1
    internship_request.refresh_from_db()
    assert internship_request.status == "approved"

@pytest.mark.django_db
def test_approve_internship_request_wrong_role(client, supervisor_user, student_user, company, academic_year):

    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship_request = InternshipRequest.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship"
    )
    response = client.post('/api/auth/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {"supervisor_id": str(supervisor_user.id)}
    response = client.post(f'/api/companies/admins/requests/approve/{internship_request.id}/', payload)
    assert response.status_code == 403
    assert response.data['error'] == "Only company admins can approve internship requests."