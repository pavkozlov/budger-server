from django.contrib import admin
from .models.organization import Organization
from .models.organization_kso import OrganizationKso
from .models.employee import Employee


admin.site.register(Organization)
admin.site.register(OrganizationKso)
admin.site.register(Employee)
