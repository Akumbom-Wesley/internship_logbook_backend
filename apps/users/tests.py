import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from apps.students.models import Student
from apps.supervisors.models import Supervisor

@pytest.mark.django_db
def test_register(client):
    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "contact": "+237623456789",
        "password": "password123",
        "role": "user"
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 201
    # Check for fields that UserSerializer returns
    assert response.data['email'] == "john@example.com"
    assert response.data['full_name'] == "John Doe"
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_login(client):
    user = User.objects.create_user(
        email="john@example.com", password="password123",
        full_name="John Doe", contact="+237623456789", role="user"
    )
    response = client.post('/api/auth/login/', {"email": "john@example.com", "password": "password123"})
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_current_user(client):
    user = User.objects.create_user(
        email="john@example.com", password="password123",
        full_name="John Doe", contact="+237623456789", role="user"
    )
    response = client.post('/api/auth/login/', {"email": "john@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    response = client.get('/api/auth/me/')
    assert response.status_code == 200
    assert response.data['email'] == "john@example.com"
    assert response.data['role'] == "user"

@pytest.mark.django_db
def test_role_selection_student(client, department):
    user = User.objects.create_user(
        email="john@example.com", password="password123",
        full_name="John Doe", contact="+237623456789", role="user"
    )
    response = client.post('/api/auth/login/', {"email": "john@example.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {
        "role": "student",
        "matricule_num": "UBa25E0001",
        "department_id": str(department.id)
    }
    response = client.post('/api/auth/select-role/', payload)
    assert response.status_code == 200
    assert response.data['message'] == "Role set to student."
    user.refresh_from_db()
    assert user.role == "student"
    assert Student.objects.count() == 1

@pytest.mark.django_db
def test_role_selection_supervisor(client, company, mocker):
    mocker.patch('apps.utils.emails.send_verification_email', return_value=None)
    user = User.objects.create_user(
        email="john@techcorp.com", password="password123",
        full_name="John Doe", contact="+237623456789", role="user"
    )
    response = client.post('/api/auth/login/', {"email": "john@techcorp.com", "password": "password123"})
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    payload = {
        "role": "supervisor",
        "company_id": str(company.id)
    }
    response = client.post('/api/auth/select-role/', payload)
    assert response.status_code == 200
    assert response.data['message'] == "Role set to supervisor."
    user.refresh_from_db()
    assert user.role == "supervisor"
    assert Supervisor.objects.count() == 1
    supervisor = Supervisor.objects.first()
    assert supervisor.status == "pending"

@pytest.mark.django_db
def test_verify_supervisor(client, company):
    user = User.objects.create_user(
        email="john@techcorp.com", password="password123",
        full_name="John Doe", contact="+237623456789", role="supervisor"
    )
    supervisor = Supervisor.objects.create(user=user, company=company, status="pending")
    response = client.get(f'/api/auth/verify-supervisor/{supervisor.id}/')
    assert response.status_code == 200
    supervisor.refresh_from_db()
    assert supervisor.status == "approved"