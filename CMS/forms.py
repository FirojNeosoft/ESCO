from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from CMS.models import *


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active']
        help_texts = {
            'is_superuser': 'Designates that this user has admin role',
            'is_staff': 'Designates that this user has staff role',
        }

    def clean_email(self):
        if not self.cleaned_data['email']:
            self._errors['email'] = self.error_class(['This field is required'])

        if self.cleaned_data['email'] and User.objects.filter(email=self.cleaned_data['email']).\
                                                               exclude(username=self.cleaned_data['username']).exists():
            self._errors['email'] = self.error_class(['This email is already used'])

        return self.cleaned_data['email']


class ApplicationMasterTypesForm(ModelForm):
    class Meta:
        model = ApplicationMasterTypes
        exclude = ('created_at', 'created_by', 'modified_at', 'modified_by')


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ('created_at', 'created_by', 'modified_at', 'modified_by')


class SurveyForm(ModelForm):
    agreement_date = forms.DateField(input_formats = ('%m/%d/%Y',), required=False,
                      widget=forms.DateInput(format = '%m/%d/%Y'))
    contract_start_date = forms.DateField(input_formats = ('%m/%d/%Y',), required=False,
                      widget=forms.DateInput(format = '%m/%d/%Y'))

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['customer'].queryset = Customer.objects.exclude(status='Delete')
            self.fields['customer_type'].queryset = ApplicationMasterTypes.objects.filter(type='Customer Type').exclude(status='Delete')
            self.fields['electric_rate_class'].queryset = ApplicationMasterTypes.objects.filter(type='Electric Rate Class').exclude(
                status='Delete')
            self.fields['gas_rate_class'].queryset = ApplicationMasterTypes.objects.filter(type='Gas Rate Class').exclude(
                status='Delete')
            self.fields['electric_utility'].queryset = ApplicationMasterTypes.objects.filter(type='Electric Utility Type').exclude(
                status='Delete')
            self.fields['gas_utility'].queryset = ApplicationMasterTypes.objects.filter(type='Gas Utility Type').exclude(status='Delete')
            self.fields['delivery_type'].queryset = ApplicationMasterTypes.objects.filter(type='Delivery Type').exclude(status='Delete')
            self.fields['passthru'].queryset = ApplicationMasterTypes.objects.filter(type='Passthru').exclude(status='Delete')
            self.fields['zone'].queryset = ApplicationMasterTypes.objects.filter(type='Zone').exclude(status='Delete')
        else:
            self.fields['customer'].queryset = Customer.objects.filter(status='Active')
            self.fields['customer_type'].queryset = ApplicationMasterTypes.objects.filter(type='Customer Type', status='Active')
            self.fields['electric_rate_class'].queryset = ApplicationMasterTypes.objects.filter(type='Electric Rate Class',
                                                                                          status='Active')
            self.fields['gas_rate_class'].queryset = ApplicationMasterTypes.objects.filter(type='Gas Rate Class',
                                                                                          status='Active')
            self.fields['electric_utility'].queryset = ApplicationMasterTypes.objects.filter(type='Electric Utility Type', status='Active')
            self.fields['gas_utility'].queryset = ApplicationMasterTypes.objects.filter(type='Gas Utility Type', status='Active')
            self.fields['delivery_type'].queryset = ApplicationMasterTypes.objects.filter(type='Delivery Type', status='Active')
            self.fields['passthru'].queryset = ApplicationMasterTypes.objects.filter(type='Passthru', status='Active')
            self.fields['zone'].queryset = ApplicationMasterTypes.objects.filter(type='Zone', status='Active')
        self.fields['survey_completed_by'].queryset = User.objects.filter(is_active = True)
        passthru = ApplicationMasterTypes.objects.get(type='Passthru', name='Not listed')
        zone = ApplicationMasterTypes.objects.get(type='Zone', name='Not listed')
        self.fields['passthru'].initial = passthru
        self.fields['zone'].initial = zone
        self.fields['green'].initial = 'No'

    class Meta:
        model = Survey
        exclude = ('gas_description', 'electric_description', 'billing_description','created_at', 'created_by',\
                   'modified_at', 'modified_by')
        widgets = {
          'service_address_line1': forms.TextInput(attrs={'placeholder': 'Line 1', 'class': 'form-control'}),
          'service_address_line2': forms.TextInput(attrs={'placeholder': 'Line 2', 'class': 'form-control'}),
          'service_address_city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
          'service_address_state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
          'service_address_zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
          'billing_address_line1': forms.TextInput(attrs={'placeholder': 'Line 1', 'class': 'form-control'}),
          'billing_address_line2': forms.TextInput(attrs={'placeholder': 'Line 2', 'class': 'form-control'}),
          'billing_address_city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
          'billing_address_state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
          'billing_address_zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
          'customer_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200 }),
          'utility_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200}),
          'gas_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200 }),
          'electric_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200}),
          'billing_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200}),
          'account_type': forms.RadioSelect(),
          'door_to_door': forms.RadioSelect(),
          'billing': forms.RadioSelect(),
          'billing_method': forms.RadioSelect(),
          'commodity_gas': forms.RadioSelect(),
          'electric': forms.RadioSelect(),
          'therm': forms.RadioSelect(),
          'tax_exempt': forms.RadioSelect(),
          'monthly_budget': forms.RadioSelect(),
        }

    def clean(self):
        gas = self.cleaned_data['commodity_gas']
        electric = self.cleaned_data['electric']
        if gas == 'Yes' and not self.cleaned_data['delivery_type']:
            self._errors['delivery_type'] = self.error_class(['This field is required'])
        if gas == 'Yes' and not self.cleaned_data['gas_price_plan']:
            self._errors['gas_price_plan'] = self.error_class(['This field is required'])
        if electric == 'Yes' and not self.cleaned_data['green']:
            self._errors['green'] = self.error_class(['This field is required'])
        if electric == 'Yes' and not self.cleaned_data['electric_price_type']:
            self._errors['electric_price_type'] = self.error_class(['This field is required'])
        if electric == 'Yes' and not self.cleaned_data['zone']:
            self._errors['zone'] = self.error_class(['This field is required'])
        if self.cleaned_data['gas_price_plan'] == 'Fixed' and not self.cleaned_data['gas_fixed_rate']:
            self._errors['gas_fixed_rate'] = self.error_class(['This field is required'])
        if self.cleaned_data['gas_price_plan'] == 'Index' and not self.cleaned_data['gas_index_rate']:
            self._errors['gas_index_rate'] = self.error_class(['This field is required'])
        if self.cleaned_data['electric_price_type'] == 'Fixed' and not self.cleaned_data['electric_fixed_rate']:
            self._errors['electric_fixed_rate'] = self.error_class(['This field is required'])
        if self.cleaned_data['electric_price_type'] == 'Index' and not self.cleaned_data['electric_index_rate']:
            self._errors['electric_index_rate'] = self.error_class(['This field is required'])
        if not self.cleaned_data['passthru']:
            self._errors['passthru'] = self.error_class(['This field is required'])
        if self.cleaned_data['utility_pool'] < 0 or self.cleaned_data['utility_pool'] > 100:
            self._errors['utility_pool'] = self.error_class(['Value should be between 0 to 100.'])
        if self.cleaned_data['electric_bandwidth_usage'] < 0 or self.cleaned_data['electric_bandwidth_usage'] > 100:
            self._errors['electric_bandwidth_usage'] = self.error_class(['Value should be between 0 to 100.'])
        if self.cleaned_data['gas_bandwidth_usage'] < 0 or self.cleaned_data['gas_bandwidth_usage'] > 100:
            self._errors['gas_bandwidth_usage'] = self.error_class(['Value should be between 0 to 100.'])


class DocForm(ModelForm):
    class Meta:
        model = Doc
        fields = ('survey', 'document')

DocFormSet = inlineformset_factory(Survey, Doc, form=DocForm, extra=1, max_num=3, validate_max=True)
