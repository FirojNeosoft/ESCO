import logging, datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin

from CMS.models import *
from CMS.forms import *
from CMS.resources import *

logger = logging.getLogger('cms_log')


class ListUsersView(LoginRequiredMixin, ListView):
    """
    List Users
    """
    model = User
    queryset = User.objects.all()
    template_name = 'user_list.html'


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


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was updated successfully"
    success_url = reverse_lazy('list_users')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('list_users')


class ListSurveyView(LoginRequiredMixin, ListView):
    """
    List Survey
    """
    model = Survey
    queryset = Survey.objects.all()
    template_name = 'list_surveys.html'


class CreateSurveyView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            survey.created_by = request.user
            survey.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_survey')
        return HttpResponseRedirect(reverse('list_surveys'))


class UpdateSurveyView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
            survey.modified_by = request.user
            survey.modified_at = datetime.datetime.now()
            survey.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_survey', pk)
        return HttpResponseRedirect(reverse('list_surveys'))


class DeleteSurveyView(LoginRequiredMixin, DeleteView):
    """
    Delete existing survey
    """
    model = Survey
    template_name = 'survey_confirm_delete.html'
    success_url = reverse_lazy('list_surveys')


class DetailSurveyView(LoginRequiredMixin, DetailView):
    model = Survey
    template_name = 'survey_detail.html'


def survey_export_csv(request):
    survey_resource = SurveyResource()
    dataset = survey_resource.export()
    # response = HttpResponse(dataset.csv, content_type='text/csv')
    # response['Content-Disposition'] = 'attachment; filename="survey.csv"'
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="survey.xls"'
    return response
