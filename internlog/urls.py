"""
URL configuration for internlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls.auth')),
    path('api/users/', include('apps.users.urls.users')),
    path('api/students/', include('apps.students.urls')),
    path('api/academic-years/', include('apps.academic_years.urls')),
    path('api/companies/admins/', include('apps.companies.urls.admin_urls')),
    path('api/internships/', include('apps.internships.urls')),
    path('api/supervisors/', include('apps.supervisors.urls')),
    path('api/departments/', include('apps.departments.urls')),
    path('api/companies/', include('apps.companies.urls.companies')),
    path('api/logbooks/', include('apps.logbooks.urls')),
    path('api/weekly-logs/', include('apps.weekly_logs.urls')),
    path('api/logbook-entries/', include('apps.logbook_entries.urls')),
    path('api/logbook-entry-photos/', include('apps.logbook_entry_photos.urls')),
    path('api/evaluations/', include('apps.evaluations.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
