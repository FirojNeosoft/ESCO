from django.contrib import admin

from CMS.models import *


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('survey_completed_by', 'customer_name', 'salesperson_name', 'created_at')

admin.site.register(Survey, SurveyAdmin)
