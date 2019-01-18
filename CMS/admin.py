from django.contrib import admin

from CMS.models import *


class ApplicationMasterTypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status')


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('survey_completed_by', 'customer_name', 'salesperson_name', 'created_at')

admin.site.register(Survey, SurveyAdmin)
admin.site.register(ApplicationMasterTypes, ApplicationMasterTypesAdmin)
