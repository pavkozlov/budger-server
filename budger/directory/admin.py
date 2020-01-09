from django.contrib import admin
from .models.entity import Entity
from .models.kso import Kso
from .models.kso import KsoEmployee
from .models.kso import KsoDepartment1, KsoDepartment2


class KsoDepartment1Admin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


admin.site.register(KsoDepartment1, KsoDepartment1Admin)


class KsoDepartment2Admin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


admin.site.register(KsoDepartment2, KsoDepartment2Admin)


class EntityAdmin(admin.ModelAdmin):
    list_filter = ('org_type_code', 'org_status_code', 'spec_event_code', 'budget_lvl_code')
    search_fields = ('title_search', 'inn')
    list_display = ('title_full', 'inn')
    hide = ['title_search', 'created', 'updated', 'head_photo_slug']

    def get_fields(self, request, obj=None):
        fields = super(EntityAdmin, self).get_fields(request)
        for hide_field in self.hide:
            if hide_field in fields:
                fields.pop(fields.index(hide_field))
        return fields


admin.site.register(Entity, EntityAdmin)


class KsoAdmin(admin.ModelAdmin):
    search_fields = ('title_search',)
    list_display = ('title_full',)
    hide = ['title_search', 'logo']

    def get_fields(self, request, obj=None):
        fields = super(KsoAdmin, self).get_fields(request)
        for hide_field in self.hide:
            if hide_field in fields:
                fields.pop(fields.index(hide_field))
        return fields


admin.site.register(Kso, KsoAdmin)


class KsoEmployeeAdmin(admin.ModelAdmin):
    list_filter = ('kso',)
    search_fields = ('name',)
    list_display = ('name', 'kso')
    hide = ['photo_slug']

    def get_fields(self, request, obj=None):
        fields = super(KsoEmployeeAdmin, self).get_fields(request)
        for hide_field in self.hide:
            if hide_field in fields:
                fields.pop(fields.index(hide_field))
        return fields


admin.site.register(KsoEmployee, KsoEmployeeAdmin)
