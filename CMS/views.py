from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from tablib import Dataset
from import_export import resources

from CMS.models import *
from CMS.forms import *
from CMS.resources import *


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


class DeleteSurveyView(DeleteView):
    """
    Delete existing survey
    """
    model = Survey
    template_name = 'survey_confirm_delete.html'
    success_url = reverse_lazy('list_surveys')


class DetailSurveyView(DetailView):
    model = Survey
    template_name = 'survey_detail.html'


def survey_export_csv(request):
    survey_resource = ExportSurveyResource()
    dataset = survey_resource.export()
    # response = HttpResponse(dataset.csv, content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="survey.csv"'
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="survey.xls"'
    return response


class ImportDataView(View):

    def get(self, request):
        return render(request, 'import.html')

    def post(self, request):
        try:
            # import pdb; pdb.set_trace()
            contract_resource = ImportSurveyResource()
            dataset = Dataset()
            new_contracts = request.FILES['myfile']

            imported_data = dataset.load(new_contracts.read())
            result = contract_resource.import_data(dataset, dry_run=True)  # Test the data import

            if not result.has_errors():
                contract_resource.import_data(dataset, dry_run=False)  # Actually import now
            return redirect('list_surveys')
        except Exception as inst:
            print(">>>", inst)
