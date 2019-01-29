import logging, datetime

from django.contrib import messages
from django.db import transaction
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from CMS.models import *
from CMS.forms import *
from CMS.resources import *
from ESCO.decorators import *

from tablib import Dataset

logger = logging.getLogger('cms_log')

@method_decorator(check_validity_of_license, name='dispatch')
class ListUsersView(LoginRequiredMixin, ListView):
    """
    List Users
    """
    model = User
    queryset = User.objects.all()
    template_name = 'user_list.html'

@method_decorator(check_validity_of_license, name='dispatch')
class CreateUserView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was created successfully"
    success_url = reverse_lazy('list_users')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password'])
            user.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_user')
        return HttpResponseRedirect(reverse('list_users'))

@method_decorator(check_validity_of_license, name='dispatch')
class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was updated successfully"
    success_url = reverse_lazy('list_users')

@method_decorator(check_validity_of_license, name='dispatch')
class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('list_users')

@method_decorator(check_validity_of_license, name='dispatch')
class ListApplicationMasterTypesView(LoginRequiredMixin, ListView):
    """
    List ApplicationMasterTypes
    """
    model = ApplicationMasterTypes
    queryset = ApplicationMasterTypes.objects.all()
    template_name = 'list_app_master_types.html'

@method_decorator(check_validity_of_license, name='dispatch')
class CreateApplicationMasterTypeView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            instance_exists = ApplicationMasterTypes.objects.filter(name=request.POST['name'],
                                                                    type=request.POST['type']).exists()
            if not instance_exists:
                survey = form.save()
                # survey.created_by = request.user
                survey.save()
            else:
                messages.error(request, 'Master type with this name and category is already exist')
                return redirect('add_master_type')
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_master_type')
        return HttpResponseRedirect(reverse('list_master_types'))

@method_decorator(check_validity_of_license, name='dispatch')
class UpdateApplicationMasterTypeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

@method_decorator(check_validity_of_license, name='dispatch')
class DeleteApplicationMasterTypeView(LoginRequiredMixin, DeleteView):
    """
    Delete existing ApplicationMasterType
    """
    model = ApplicationMasterTypes
    template_name = 'app_master_type_confirm_delete.html'
    success_url = reverse_lazy('list_master_types')

@method_decorator(check_validity_of_license, name='dispatch')
class ListSurveyView(LoginRequiredMixin, ListView):
    """
    List Survey
    """
    model = Survey
    queryset = Survey.objects.all()
    template_name = 'list_surveys.html'

@method_decorator(check_validity_of_license, name='dispatch')
class CreateSurveyView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new survey
    """
    model = Survey
    form_class = SurveyForm
    template_name = 'survey_form.html'
    success_message = "Survey was created successfully"
    success_url = reverse_lazy('list_surveys')

    def get_context_data(self, **kwargs):
        data = super(CreateSurveyView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['docs'] = DocFormSet(self.request.POST, self.request.FILES)
        else:
            data['docs'] = DocFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        docs = context['docs']
        with transaction.atomic():
            if docs.is_valid():
                self.object = form.save()
                self.object.created_by = self.request.user
                self.object.save()
                docs.instance = self.object
                docs.save()
            else:
                logger.error(docs.errors)
                messages.error(self.request, "Error occured while uploading documents")
                return redirect('add_survey')
        return super(CreateSurveyView, self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         survey = form.save()
    #         # survey.created_by = request.user
    #         survey.save()
    #     else:
    #         logger.error(form.errors)
    #         messages.error(request, form.errors)
    #         return redirect('add_survey')
    #     return HttpResponseRedirect(reverse('list_surveys'))

@method_decorator(check_validity_of_license, name='dispatch')
class UpdateSurveyView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing survey
    """
    model = Survey
    form_class = SurveyForm
    template_name = 'survey_form.html'
    success_message = "Survey was updated successfully"
    success_url = reverse_lazy('list_surveys')

    def get_context_data(self, **kwargs):
        data = super(UpdateSurveyView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['docs'] = DocFormSet(self.request.POST, self.request.FILES, instance=self.object)
            data['docs'].full_clean()
        else:
            data['docs'] = DocFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        docs = context['docs']
        with transaction.atomic():
            self.object = form.save()
            self.object.modified_by = self.request.user
            self.object.modified_at = datetime.datetime.now()
            self.object.save()
            if docs.is_valid():
                docs.instance = self.object
                docs.save()
            else:
                logger.error(docs.errors)
                messages.error(self.request, "Error occured while uploading documents")
                return redirect('update_survey', self.object.id)
        return super(UpdateSurveyView, self).form_valid(form)

    # def post(self, request, pk):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     self.object = Survey.objects.get(id=pk)
    #     form = self.get_form()
    #     if form.is_valid():
    #         survey = form.save()
    #         # survey.modified_by = request.user
    #         survey.modified_at = datetime.datetime.now()
    #         survey.save()
    #     else:
    #         logger.error(form.errors)
    #         messages.error(request, form.errors)
    #         return redirect('update_survey', pk)
    #     return HttpResponseRedirect(reverse('list_surveys'))

@method_decorator(check_validity_of_license, name='dispatch')
class DeleteSurveyView(LoginRequiredMixin, DeleteView):
    """
    Delete existing survey
    """
    model = Survey
    template_name = 'survey_confirm_delete.html'
    success_url = reverse_lazy('list_surveys')

@method_decorator(check_validity_of_license, name='dispatch')
class DetailSurveyView(LoginRequiredMixin, DetailView):
    model = Survey
    template_name = 'survey_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['passthru'] = kwargs['object'].passthru.all()
        context['zones'] = kwargs['object'].zone.all()
        context['doc_list'] = Doc.objects.filter(survey=kwargs['object'])
        return context

@login_required
@check_validity_of_license
def survey_export_csv(request):
    survey_resource = ExportSurveyResource()
    dataset = survey_resource.export()
    # response = HttpResponse(dataset.csv, content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="survey.csv"'
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="survey.xls"'
    return response

@method_decorator(check_validity_of_license, name='dispatch')
class ImportDataView(LoginRequiredMixin, View):

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
