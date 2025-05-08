Below is a `README.md` file in Markdown format that documents the `internship_logbook_backend` project based on all the work we’ve done. It includes setup instructions, project structure, API endpoints, testing instructions, and more.

---

# Internship Logbook Backend

This is the backend for the Internship Logbook application, built with **Django** and **Django REST Framework**. The application manages internship workflows for students, supervisors, company admins, and school administrators. It supports user registration, role-based workflows, internship requests, and approval processes.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Future Improvements](#future-improvements)

---

## Features
- **User Management**:
  - Role-based authentication: `student`, `supervisor`, `company_admin`, `lecturer`, `super_admin`.
  - Registration, login, and role selection with JWT authentication.
  - Email verification for supervisors (pending approval).

- **Internship Workflow**:
  - Students can create internship requests to companies.
  - Company admins can view and approve requests, assigning a supervisor.
  - Internship status: `waiting` (if start date is future), `ongoing`, `completed`, or `cancelled`.
  - School admins can assign lecturers to internships (future feature).

- **Security**:
  - Role-based permissions for all endpoints.
  - Email domain validation for supervisors.
  - JWT authentication for secure access.

- **Testing**:
  - Unit tests using `pytest`.
  - Postman collection for manual API testing.

---

## Tech Stack
- **Backend Framework**: Django 5.x, Django REST Framework
- **Authentication**: `rest_framework_simplejwt` for JWT-based authentication
- **Database**: SQLite (default; can be swapped for PostgreSQL)
- **Testing**: `pytest`, `pytest-django`
- **Environment Management**: `python-dotenv`
- **Email**: Django’s email system (SMTP with Gmail for development)

---

## Project Structure
```
internship_logbook_backend/
├── apps/
│   ├── academic_years/
│   │   ├── models.py
│   │   └── serializers.py
│   ├── companies/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── tests.py
│   ├── core/
│   │   └── models.py
│   ├── departments/
│   │   ├── models.py
│   │   └── serializers.py
│   ├── academic_years/
│   │   ├── models.py
│   │   └── serializers.py
│   ├── internships/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── tests.py
│   ├── lecturers/
│   │   └── models.py
│   ├── school/
│   │   └── models.py
│   ├── students/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── supervisors/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── utils/
│       ├── email.py
│       └── tasks.py
├── internlog/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── .env
├── manage.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### **Prerequisites**
- Python 3.12.x
- Virtualenv (optional but recommended)
- Git
- Postman (for API testing)

### **Steps**
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd internship_logbook_backend
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the project root:
     ```
     SECRET_KEY=your-secret-key
     DEBUG=True
     EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
     EMAIL_HOST='smtp.gmail.com'
     EMAIL_PORT=587
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER='your-email@gmail.com'
     EMAIL_HOST_PASSWORD='your-app-password'
     DEFAULT_FROM_EMAIL='your-email@gmail.com'
     ```
   - Replace `your-email@gmail.com` and `your-app-password` with your Gmail credentials (use an App Password if 2FA is enabled).

5. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://localhost:8000`.

---

## API Endpoints

### **Authentication**
- **POST** `/api/users/register/`: Register a new user.
  - Body: `{"full_name": "John Doe", "email": "john@example.com", "contact": "+237623456789", "password": "password123", "role": "user"}`
- **POST** `/api/users/login/`: Login and obtain JWT tokens.
  - Body: `{"email": "john@example.com", "password": "password123"}`
- **POST** `/api/users/token/refresh/`: Refresh JWT token.
- **GET** `/api/users/me/`: Get details of the logged-in user (requires authentication).
- **POST** `/api/users/select-role/`: Select role after registration.
  - Body: `{"role": "student", "matricule_num": "UBa25E0001", "department_id": "<uuid>"}` (or `{"role": "supervisor", "company_id": "<uuid>"}`, or `{"role": "company_admin", "company_id": "<uuid>"}`)

### **Student Endpoints**
- **GET** `/api/students/`: List all students (admin only).
- **POST** `/api/students/requests/create/`: Create an internship request.
  - Body: `{"company": "<company_id>", "academic_year": "<academic_year_id>", "start_date": "2025-06-01T00:00:00Z", "end_date": "2025-08-01T00:00:00Z", "job_description": "Software development internship"}`
- **GET** `/api/students/requests/`: List the student’s internship requests.

### **Company Admin Endpoints**
- **GET** `/api/company-admins/requests/`: List pending internship requests for the company.
- **POST** `/api/company-admins/requests/approve/<request_id>/`: Approve an internship request and assign a supervisor.
  - Body: `{"supervisor_id": "<supervisor_id>"}`

### **Supervisor Endpoints**
- (Previously used for approving requests; now managed by company admins.)

---

## Testing

### **Unit Tests**
1. Install testing dependencies:
   ```bash
   pip install pytest pytest-django
   ```
2. Run tests:
   ```bash
   pytest
   ```

### **Postman Testing**
1. Import the Postman collection (`InternLog_API.postman_collection.json`) provided in the project.
2. Set up environment variables in Postman:
   - `base_url`: `http://localhost:8000`
   - `access_token`, `department_id`, `company_id`, `academic_year_id`, `request_id`, `supervisor_user_id`
3. Test the API endpoints in the following order:
   - Register and login as a student.
   - Select role as student.
   - Create an internship request.
   - Register and login as a company admin.
   - Approve the internship request with a supervisor ID.

---

## Future Improvements
- **Lecturer Assignment**: Implement endpoints for school admins to assign lecturers to internships.
- **Auto-Deletion Task**: Implement a task to delete unapproved supervisors after 7 days using `django-celery-beat`.
- **Notifications**: Add more email notifications (e.g., for students when requests are approved).
- **Pagination**: Add pagination to list endpoints for better performance.
- **Production Deployment**: Configure for production (PostgreSQL, Gunicorn, Nginx).

---

## License
This project is licensed under the MIT License.

---

This `README.md` provides a comprehensive overview of the project, including setup, usage, and testing instructions. Let me know if you’d like to add more details or proceed with the next steps (e.g., auto-deletion task)!