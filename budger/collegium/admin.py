from django.contrib import admin
from .models import Meeting, Speaker


# class MeetingAdmin(admin.ModelAdmin):
#     list_filter = ('status',)
#     list_display = ('exec_date', 'status')
#
#
# admin.site.register(Meeting, MeetingAdmin)
#
#
# class SpeakerAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'meeting')
#
#
# admin.site.register(Speaker, SpeakerAdmin)
