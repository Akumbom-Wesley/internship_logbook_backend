from django.contrib import admin

from apps.companies.models import Company, CompanyAdmin

admin.site.register(Company)
admin.site.register(CompanyAdmin)