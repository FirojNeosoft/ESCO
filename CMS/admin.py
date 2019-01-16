from django.contrib import admin

from CMS.models import *


class PassthruAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('survey_completed_by', 'customer_name', 'salesperson_name', 'created_at')

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
            obj.modified_at = datetime.datetime.now()
        else:
            obj.created_by = request.user
        obj.save()

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Passthru, PassthruAdmin)
admin.site.register(Zone, ZoneAdmin)
