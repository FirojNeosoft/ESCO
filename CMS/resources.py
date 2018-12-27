from import_export import resources
from import_export.fields import Field
from CMS.models import *


class SurveyResource(resources.ModelResource):
    survey_completed_by = Field(attribute='survey_completed_by')
    class Meta:
        model = Survey
        exclude = ('id',)
        widgets = {
                'agreement_date': {'format': '%m/%d/%Y'},
                'contract_start_date': {'format': '%m/%d/%Y'},
                'usage_from_date': {'format': '%m/%d/%Y'},
                'usage_to_date': {'format': '%m/%d/%Y'},
                'created_at': {'format': '%m/%d/%Y %I:%M %p'},
                }
    def dehydrate_survey_completed_by(self, survey):
        return '%s' % (survey.survey_completed_by.username)
