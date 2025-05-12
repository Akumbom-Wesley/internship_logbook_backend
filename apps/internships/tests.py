import pytest
from apps.internships.models import Internship
from apps.users.models import User
from apps.companies.models import CompanyAdmin
from django.utils import timezone
from datetime import timedelta

@pytest.fixture
def internship(student_user, company, academic_year, supervisor_user):
    return Internship.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=timezone.now() + timedelta(days=1),
        end_date=timezone.now() + timedelta(days=60),
        job_description="Test internship",
        supervisor=supervisor_user,
        status="waiting"
    )

@pytest.fixture
def internship2(student_user, company, academic_year, supervisor_user):
    return Internship.objects.create(
        student=student_user, company=company, academic_year=academic_year,
        start_date=timezone.now() + timedelta(days=1),
        end_date=timezone.now() + timedelta(days=60),
        job_description="Test internship 2",
        supervisor=supervisor_user,
        status="waiting"
    )

@pytest.mark.django_db
def test_list_internships(client, company_admin_user, internship):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Get internships for the company
    company_id = company_admin_user.company.id
    response = client.get(f'/api/internships/{company_id}/list')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['job_description'] == "Test internship"

@pytest.mark.django_db
def test_filter_internships_by_status(client, company_admin_user, internship):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Get internships filtered by status
    company_id = company_admin_user.company.id
    response = client.get(f'/api/internships/{company_id}/list?status=waiting')

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['status'] == "waiting"

    # Try with a status that shouldn't return results
    response = client.get(f'/api/internships/{company_id}/list?status=completed')
    assert response.status_code == 200
    assert len(response.data) == 0

@pytest.mark.django_db
def test_filter_internships_by_academic_year(client, company_admin_user, internship, academic_year):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Get internships filtered by academic year
    company_id = company_admin_user.company.id
    year_id = academic_year.id
    response = client.get(f'/api/internships/{company_id}/list?academic_year={year_id}')

    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_retrieve_internship(client, company_admin_user, internship):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Get specific internship
    response = client.get(f'/api/internships/{internship.id}/')

    assert response.status_code == 200
    assert response.data['job_description'] == "Test internship"

@pytest.mark.django_db
def test_update_internship(client, company_admin_user, internship, supervisor_user, lecturer_user):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {
        "job_description": "Updated internship",
        "status": "completed",
        "supervisor": str(supervisor_user.id),
        "lecturer": str(lecturer_user.id)
    }
    response = client.patch(f'/api/internships/{internship.id}/update/', payload, format='json')

    assert response.status_code == 200
    assert response.data['job_description'] == "Updated internship"
    assert response.data['status'] == "completed"

@pytest.mark.django_db
def test_update_internship_wrong_company(client, internship, other_company):
    # Create another company admin for the other company
    user = User.objects.create_user(
        email="admin2@othercorp.com", password="password123",
        full_name="Other Admin", contact="+237623456790", role="company_admin"
    )
    other_admin = CompanyAdmin.objects.create(user=user, company=other_company)

    # Login as the other company admin
    response = client.post('/api/auth/login/', {"email": "admin2@othercorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {
        "job_description": "Should not update",
        "status": "completed"
    }
    response = client.patch(f'/api/internships/{internship.id}/update/', payload, format='json')

    assert response.status_code == 403
    assert "not belong to your company" in response.data["error"]

@pytest.mark.django_db
def test_delete_internship_company_admin(client, company_admin_user, internship):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.delete(f'/api/internships/{internship.id}/delete/')

    assert response.status_code == 204
    assert Internship.objects.count() == 0

@pytest.mark.django_db
def test_delete_internship_super_admin(client, super_admin_user, internship):
    # Login as super admin
    response = client.post('/api/auth/login/', {"email": "superadmin@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.delete(f'/api/internships/{internship.id}/delete/')

    assert response.status_code == 204
    assert Internship.objects.count() == 0

@pytest.mark.django_db
def test_delete_internship_wrong_company(client, internship, other_company):
    # Create another company admin for the other company
    user = User.objects.create_user(
        email="admin2@othercorp.com", password="password123",
        full_name="Other Admin", contact="+237623456790", role="company_admin"
    )
    other_admin = CompanyAdmin.objects.create(user=user, company=other_company)

    # Login as the other company admin
    response = client.post('/api/auth/login/', {"email": "admin2@othercorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    response = client.delete(f'/api/internships/{internship.id}/delete/')

    assert response.status_code == 403
    assert "not belong to your company" in response.data["error"]

@pytest.mark.django_db
def test_bulk_update_internships(client, company_admin_user, internship, internship2):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    company_id = company_admin_user.company.id
    payload = {
        "status": "completed"
    }
    response = client.patch(f'/api/internships/{company_id}/bulk-update/', payload, format='json')

    assert response.status_code == 200
    assert response.data['message'] == f"Updated status to 'completed' for 2 internships."
    assert Internship.objects.filter(status="completed").count() == 2

@pytest.mark.django_db
def test_bulk_update_wrong_company(client, company_admin_user, internship, other_company):
    # Login as company admin
    response = client.post('/api/auth/login/', {"email": "admin@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Try to update internships for a different company
    response = client.patch(f'/api/internships/{other_company.id}/bulk-update/',
                            {"status": "completed"}, format='json')

    assert response.status_code == 403
    assert "only update internships for your company" in response.data['error']

@pytest.mark.django_db
def test_forbidden_access_student(client, student_user, internship):
    # Login as student
    response = client.post('/api/auth/login/', {"email": "student@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    company_id = internship.company.id

    # Try to access company internships
    response = client.get(f'/api/internships/{company_id}/list')
    assert response.status_code == 403

    # Try to update an internship
    response = client.patch(f'/api/internships/{internship.id}/update/',
                            {"status": "completed"}, format='json')
    assert response.status_code == 403

    # Try to delete an internship
    response = client.delete(f'/api/internships/{internship.id}/delete/')
    assert response.status_code == 403

    # Try bulk update
    response = client.patch(f'/api/internships/{company_id}/bulk-update/',
                            {"status": "completed"}, format='json')
    assert response.status_code == 403