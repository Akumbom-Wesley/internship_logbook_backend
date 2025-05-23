import pytest
from django.utils import timezone
from datetime import datetime
from apps.internships.models import Internship
from apps.supervisors.models import Supervisor
from apps.users.models import User

@pytest.mark.django_db
def test_supervisor_assigned_internships(client, supervisor_user, student_user, company, academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship = Internship.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship",
        supervisor=supervisor_user, status="waiting"
    )

    response = client.post('/api/auth/login/', {"email": "supervisor@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/supervisors/assigned-internships/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['job_description'] == "Test internship"


@pytest.mark.django_db
def test_supervisor_assigned_internships_unapproved(client, unapproved_supervisor_user, student_user, company,
                                                    academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    internship = Internship.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship",
        supervisor=unapproved_supervisor_user, status="waiting"
    )

    response = client.post('/api/auth/login/', {"email": "unapproved@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/supervisors/assigned-internships/')
    assert response.status_code == 403
    assert response.data['error'] == "Only approved supervisors can view assigned internships."


@pytest.mark.django_db
def test_supervisor_assigned_internships_wrong_role(client, student_user, company, academic_year):
    aware_start = timezone.make_aware(datetime(2025, 6, 1))
    aware_end = timezone.make_aware(datetime(2025, 8, 1))

    supervisor_user = Supervisor.objects.create(
        user=User.objects.create_user(
            email="supervisor@techcorp.com", password="password123",
            full_name="Supervisor User", contact="+237623456789", role="supervisor"
        ),
        company=company, status="approved"
    )
    internship = Internship.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=aware_start, end_date=aware_end, job_description="Test internship",
        supervisor=supervisor_user, status="waiting"
    )

    response = client.post('/api/auth/login/', {"email": "student@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.get('/api/supervisors/assigned-internships/')
    assert response.status_code == 403
    assert response.data['error'] == "Only supervisors can view assigned internships."