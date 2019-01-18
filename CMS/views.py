import logging, datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin

from CMS.models import *
from CMS.forms import *
from CMS.resources import *

logger = logging.getLogger('cms_log')


class ListApplicationMasterTypesView(ListView):
    """
    List ApplicationMasterTypes
    """
    model = ApplicationMasterTypes
    queryset = ApplicationMasterTypes.objects.all()
    template_name = 'list_app_master_types.html'


class CreateApplicationMasterTypeView(SuccessMessageMixin, CreateView):
    """
    Create new ApplicationMasterType
    """
    model = ApplicationMasterTypes
    form_class = ApplicationMasterTypesForm
    template_name = 'app_master_type_form.html'
    success_message = "Type was created successfully"
    success_url = reverse_lazy('list_master_types')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            survey = form.save()
            # survey.created_by = request.user
            survey.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_master_type')
        return HttpResponseRedirect(reverse('list_master_types'))


class UpdateApplicationMasterTypeView(SuccessMessageMixin, UpdateView):
    """
    Update existing ApplicationMasterType
    """
    model = ApplicationMasterTypes
    form_class = ApplicationMasterTypesForm
    template_name = 'app_master_type_form.html'
    success_message = "Type was updated successfully"
    success_url = reverse_lazy('list_master_types')

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = ApplicationMasterTypes.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            survey = form.save()
            # survey.modified_by = request.user
            survey.modified_at = datetime.datetime.now()
            survey.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_master_type', pk)
        return HttpResponseRedirect(reverse('list_master_types'))


class DeleteApplicationMasterTypeView(DeleteView):
    """
    Delete existing ApplicationMasterType
    """
    model = ApplicationMasterTypes
    template_name = 'app_master_type_confirm_delete.html'
    success_url = reverse_lazy('list_master_types')


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

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            survey = form.save()
            # survey.created_by = request.user
            survey.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_survey')
        return HttpResponseRedirect(reverse('list_surveys'))


class UpdateSurveyView(SuccessMessageMixin, UpdateView):
    """
    Update existing survey
    """
    model = Survey
    form_class = SurveyForm
    template_name = 'survey_form.html'
    success_message = "Survey was updated successfully"
    success_url = reverse_lazy('list_surveys')

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Survey.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            survey = form.save()
            # survey.modified_by = request.user
            survey.modified_at = datetime.datetime.now()
            survey.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_survey', pk)
        return HttpResponseRedirect(reverse('list_surveys'))


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
