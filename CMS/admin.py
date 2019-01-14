from django.contrib import admin

from CMS.models import *

class PassthruAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('survey_completed_by', 'customer_name', 'salesperson_name', 'created_at')

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Passthru, PassthruAdmin)
admin.site.register(Zone, ZoneAdmin)
