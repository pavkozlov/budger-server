from django.contrib import admin
from .models import Annual, Event


class AnnualAdmin(admin.ModelAdmin):
    list_filter = ('year', 'status')
    list_display = ('year', 'status')


admin.site.register(Annual, AnnualAdmin)


class EventAdmin(admin.ModelAdmin):
    list_filter = ('group', 'type', 'mode',)
    list_display = ('title', 'exec_from', 'exec_to')
    search_fields = ('title',)


admin.site.register(Event, EventAdmin)
