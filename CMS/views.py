from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from CMS.models import *
from CMS.forms import *


class ListSurveyView(ListView):
    """
    List Survey
    """
    model = Survey
    queryset = Survey.objects.all()
    template_name = 'list_surveys.html'


class CreateSurveyView(SuccessMessageMixin, CreateView):
    """
    Create new survey
    """
    model = Survey
    form_class = SurveyForm
    template_name = 'survey_form.html'
    success_message = "Survey was created successfully"
    success_url = reverse_lazy('list_surveys')


class UpdateSurveyView(SuccessMessageMixin, UpdateView):
    """
    Update existing survey
    """
    model = Survey
    form_class = SurveyForm
    template_name = 'survey_form.html'
    success_message = "Survey was updated successfully"
    success_url = reverse_lazy('list_surveys')


class DeleteTaskView(DeleteView):
    """
    Delete existing survey
    """
    model = Survey
    template_name = 'survey_confirm_delete.html'
    success_url = reverse_lazy('list_surveys')
