import pandas as pd
import logging, datetime, os

from django.contrib import messages
from django.db import transaction
from django.db.models import Sum, Avg, Count, Min, Max
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from CMS.models import *
from CMS.forms import *
from CMS.utils import *
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
    form_class = UserForm
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
    form_class = UserForm
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
    queryset = ApplicationMasterTypes.objects.exclude(status='Delete')
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
                master_type = form.save()
                master_type.created_by = request.user
                master_type.save()
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
            master_type = form.save()
            master_type.modified_by = request.user
            master_type.modified_at = datetime.datetime.now()
            master_type.save()
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
class ListCustomerView(LoginRequiredMixin, ListView):
    """
    List Customer
    """
    model = Customer
    queryset = Customer.objects.exclude(status='Delete')
    paginate_by = 1
    template_name = 'customer_list.html'

@method_decorator(check_validity_of_license, name='dispatch')
class CreateCustomerView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new customer
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_form.html'
    success_message = "Customer was created successfully"
    success_url = reverse_lazy('list_customers')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            customer = form.save()
            customer.created_by = request.user
            customer.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_customer')
        return HttpResponseRedirect(reverse('list_customers'))


@method_decorator(check_validity_of_license, name='dispatch')
class UpdateCustomerView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing customer
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'customer_form.html'
    success_message = "Customer was updated successfully"
    success_url = reverse_lazy('list_customers')

    def post(self, request, pk):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = Customer.objects.get(id=pk)
        form = self.get_form()
        if form.is_valid():
            customer = form.save()
            customer.modified_by = request.user
            customer.modified_at = datetime.datetime.now()
            customer.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('update_customer', pk)
        return HttpResponseRedirect(reverse('list_customers'))


@method_decorator(check_validity_of_license, name='dispatch')
class DeleteCustomerView(LoginRequiredMixin, DeleteView):
    """
    Delete existing customer
    """
    model = Customer
    template_name = 'customer_confirm_delete.html'
    success_url = reverse_lazy('list_customers')


@method_decorator(check_validity_of_license, name='dispatch')
class ListSurveyView(LoginRequiredMixin, ListView):
    """
    List Survey
    """
    model = Survey
    queryset = Survey.objects.all()
    paginate_by = 2
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
            data['customers'] = Customer.objects.filter(status='Active')
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
            contract_resource = ImportSurveyResource()
            dataset = Dataset()
            new_contracts = request.FILES['myfile']

            imported_data = dataset.load(new_contracts.read())
            result = contract_resource.import_data(dataset, dry_run=True)  # Test the data import

            if not result.has_errors():
                contract_resource.import_data(dataset, dry_run=False)  # Actually import now
            return redirect('list_surveys')
        except Exception as inst:
            logger.error(inst)


class CustomerSummaryReportView(LoginRequiredMixin, View):
    """
    Customer summary report
    """
    def get(self, request):
        form = SearchReportForm()
        customer_types = ApplicationMasterTypes.objects.filter(type='Customer Type').exclude(status='Delete')
        utility_types = ApplicationMasterTypes.objects.filter(type='Electric Utility Type').exclude(status='Delete')
        return render(request, 'customer_summary_report.html', {'form': form, 'customer_types': customer_types, 'utility_types':utility_types })

    def post(self, request):
        try:
            form = SearchReportForm(request.POST)
            page = request.GET.get('page', 1)
            if form.is_valid():
                contracts = get_contracts(form.cleaned_data['commodity'], form.cleaned_data['price_type'], form.cleaned_data['term'],\
                         form.cleaned_data['utility_type'], form.cleaned_data['account_type'], form.cleaned_data['customer_type'])
                if 'submit_btn' in request.POST:
                    paginator = Paginator(contracts, 10)
                    try:
                        result = paginator.page(page)
                    except PageNotAnInteger:
                        result = paginator.page(1)
                    except EmptyPage:
                        result = paginator.page(paginator.num_pages)
                    return render(request, 'customer_summary_report.html', {'form': form, 'result': result})
                else:
                    new_contracts = contracts.values('customer__name', 'customer_type__name', 'electric',
                                                     'commodity_gas', 'electric_price_type', 'gas_price_plan',
                                                     'electric_fixed_rate', 'electric_index_rate', 'gas_fixed_rate',
                                                     'gas_index_rate', 'agreement_length', 'electric_utility__name',
                                                     'gas_utility__name', 'account_type', 'billing')
                    df = pd.DataFrame(list(new_contracts))
                    path = 'docs/customer_report.xlsx'
                    df.to_excel(path)
                    response = HttpResponse(open(path, "rb"), content_type='application/xlsx')
                    response['Content-Disposition'] = 'attachment; filename="docs/customer_report.xlsx"'
                    return response
                    # return Render.pdf_file('customer_summary_report_tpl.html', { 'result': contracts })
            else:
                return render(request, 'customer_summary_report.html', {'form': form, 'messages': form.errors})
        except Exception as e:
            logger.error("{}, error occured while searching customer summary report.".format(e))
            messages.error(request, "Error occured while searching customer summary report.")
            return redirect('customer_summary_report')


class CustomerTypeSummaryReportView(LoginRequiredMixin, View):
    """
    Customer type summary report
    """
    def get(self, request):
        form = SearchReportForm()
        customer_types = ApplicationMasterTypes.objects.filter(type='Customer Type').exclude(status='Delete')
        utility_types = ApplicationMasterTypes.objects.filter(type='Electric Utility Type').exclude(status='Delete')
        return render(request, 'customer_type_summary_report.html', {'form': form, 'customer_types': customer_types, 'utility_types':utility_types })

    def post(self, request):
        try:
            form = SearchReportForm(request.POST)
            page = request.GET.get('page', 1)
            if form.is_valid():
                contracts = get_contracts(form.cleaned_data['commodity'], form.cleaned_data['price_type'],
                                          form.cleaned_data['term'], \
                                          form.cleaned_data['utility_type'], form.cleaned_data['account_type'],
                                          form.cleaned_data['customer_type'])
                grp_contracts = []
                if form.cleaned_data['commodity'] == 'Electric' or form.cleaned_data['commodity'] == 'All':
                    grp_contracts.extend(contracts.values('account_type', 'electric_utility__name', 'electric', 'electric_price_type', 'billing').\
                        annotate(avg_term=Avg('agreement_length'), count_billing=Count('billing')
                                 ))

                if form.cleaned_data['commodity'] == 'Gas' or form.cleaned_data['commodity'] == 'All':
                    grp_contracts.extend(contracts.values('account_type', 'gas_utility__name', 'commodity_gas', 'gas_price_plan', 'billing').\
                        annotate(avg_term=Avg('agreement_length'), count_billing=Count('billing')
                                 ))
                if 'submit_btn' in request.POST:
                    paginator = Paginator(grp_contracts, 10)
                    try:
                        result = paginator.page(page)
                    except PageNotAnInteger:
                        result = paginator.page(1)
                    except EmptyPage:
                        result = paginator.page(paginator.num_pages)
                    return render(request, 'customer_type_summary_report.html', {'form': form, 'result': result})
                else:
                    df = pd.DataFrame(list(grp_contracts))
                    path = 'docs/customer_type_summary_report.xlsx'
                    df.to_excel(path)
                    response = HttpResponse(open(path, "rb"), content_type='application/xlsx')
                    response['Content-Disposition'] = 'attachment; filename="docs/customer_type_summary_report.xlsx"'
                    return response
                    # return Render.pdf_file('customer_type_summary_report_tpl.html', {'result': grp_contracts })
            else:
                return render(request, 'customer_type_summary_report.html', {'form': form, 'messages': form.errors})
        except Exception as e:
            logger.error("{}, error occured while searching customer type summary report.".format(e))
            messages.error(request, "Error occured while searching customer type summary report.")
            return redirect('customer_type_summary_report')


class LdcSummaryReportView(LoginRequiredMixin, View):
    """
    ldc summary report
    """
    def get(self, request):
        form = SearchReportForm()
        customer_types = ApplicationMasterTypes.objects.filter(type='Customer Type').exclude(status='Delete')
        utility_types = ApplicationMasterTypes.objects.filter(type='Electric Utility Type').exclude(status='Delete')
        return render(request, 'ldc_summary_report.html', {'form': form, 'customer_types': customer_types, 'utility_types':utility_types })

    def post(self, request):
        try:
            form = SearchReportForm(request.POST)
            page = request.GET.get('page', 1)
            if form.is_valid():
                contracts = get_contracts(form.cleaned_data['commodity'], form.cleaned_data['price_type'],
                                          form.cleaned_data['term'], \
                                          form.cleaned_data['utility_type'], form.cleaned_data['account_type'],
                                          form.cleaned_data['customer_type'])
                grp_contracts = []
                if form.cleaned_data['commodity'] == 'Electric' or form.cleaned_data['commodity'] == 'All':
                    grp_contracts.extend(contracts.values('electric', 'electric_utility__name', 'electric_price_type').\
                        annotate(count_customer=Count('customer'), avg_term=Avg('agreement_length'),\
                                 sum_fix=Sum('electric_fixed_rate'), sum_index=Sum('electric_index_rate'), \
                                 min_fix=Min('electric_fixed_rate'), min_index=Min('electric_index_rate'), \
                                 max_fix=Max('electric_fixed_rate'), max_index=Max('electric_index_rate'), \
                                 ))

                if form.cleaned_data['commodity'] == 'Gas' or form.cleaned_data['commodity'] == 'All':
                    grp_contracts.extend(contracts.values('commodity_gas', 'gas_utility__name', 'gas_price_plan').\
                        annotate(count_customer=Count('customer'), avg_term=Avg('agreement_length'),\
                                 sum_fix=Sum('gas_fixed_rate'), sum_index=Sum('gas_index_rate'), \
                                 min_fix=Min('gas_fixed_rate'), min_index=Min('gas_index_rate'), \
                                 max_fix=Max('gas_fixed_rate'), max_index=Max('gas_index_rate'), \
                                 ))
                if 'submit_btn' in request.POST:
                    paginator = Paginator(grp_contracts, 10)
                    try:
                        result = paginator.page(page)
                    except PageNotAnInteger:
                        result = paginator.page(1)
                    except EmptyPage:
                        result = paginator.page(paginator.num_pages)
                    return render(request, 'ldc_summary_report.html', {'form': form, 'result': result})
                else:
                    df = pd.DataFrame(list(grp_contracts))
                    path = 'docs/ldc_report.xlsx'
                    df.to_excel(path)
                    response = HttpResponse(open(path, "rb"), content_type='application/xlsx')
                    response['Content-Disposition'] = 'attachment; filename="docs/ldc_report.xlsx"'
                    return response
                    #return Render.pdf_file('ldc_summary_report_tpl.html', {'result': grp_contracts})
            else:
                return render(request, 'ldc_summary_report.html', {'form': form, 'messages': form.errors})
        except Exception as e:
            logger.error("{}, error occured while searching customer summary report.".format(e))
            messages.error(request, "Error occured while searching customer summary report.")
            return redirect('ldc_summary_report')
