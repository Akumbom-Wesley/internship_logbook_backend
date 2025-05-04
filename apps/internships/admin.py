from django.contrib import admin

from apps.internships.models import Internship, InternshipRequest

admin.site.register(Internship)
admin.site.register(InternshipRequest)