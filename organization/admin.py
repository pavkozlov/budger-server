from django.contrib import admin
from organization.models.organization_common import OrganizationCommon
from organization.models.organization_kso import OrganizationKso
from organization.models.employee import Employee


admin.site.register(OrganizationCommon)
admin.site.register(OrganizationKso)
admin.site.register(Employee)
