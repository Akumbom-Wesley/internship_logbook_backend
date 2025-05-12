import pytest
from rest_framework.test import APIClient
from apps.users.models import User
from apps.students.models import Student
from apps.departments.models import Department, School
from apps.companies.models import Company, CompanyAdmin
from apps.supervisors.models import Supervisor
from apps.academic_years.models import AcademicYear
from apps.internships.models import InternshipRequest, Internship

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def super_admin_user():
    return User.objects.create_superuser(
        full_name="Super Admin",
        email="superadmin@example.com",
        password="password123",
        contact="678365249",
        role="super_admin"
    )

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
def other_company():
    return Company.objects.create(
        name="Other Corp", address="456 Street", contact="+237623456789",
        email="contact@othercorp.com", division="HR", designation="Manager"
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
    return Supervisor.objects.create(user=user, company=company, status="approved")

@pytest.fixture
def unapproved_supervisor_user(company):
    user = User.objects.create_user(
        email="unapproved@techcorp.com", password="password123",
        full_name="Unapproved Supervisor", contact="+237623456789", role="supervisor"
    )
    return Supervisor.objects.create(user=user, company=company, status="pending")

@pytest.fixture
def lecturer_user(department):
    from apps.users.models import User
    from apps.lecturers.models import Lecturer

    user = User.objects.create_user(
        email="lecturer@example.com",
        password="password123",
        full_name="Lecturer User",
        contact="+237623456789",
        role="lecturer"
    )
    return Lecturer.objects.create(user=user, department=department, school="Science")
