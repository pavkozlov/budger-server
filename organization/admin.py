from django.contrib import admin
from organization.models.organization import Organization
from organization.models.organization_kso import OrganizationKso
from organization.models.employee import Employee


admin.site.register(Organization)
admin.site.register(OrganizationKso)
admin.site.register(Employee)
