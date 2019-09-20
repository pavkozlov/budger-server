from django.contrib import admin
from .models import OrganizationCommon, OrganizationKso, Employee


admin.site.register(OrganizationCommon)
admin.site.register(OrganizationKso)
admin.site.register(Employee)
