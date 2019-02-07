from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import User

from django.forms.models import inlineformset_factory

from CMS.models import *


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_staff']

    def clean(self):
        if not self.cleaned_data['email']:
            self._errors['email'] = self.error_class(['This field is required'])


class ApplicationMasterTypesForm(ModelForm):
    class Meta:
        model = ApplicationMasterTypes
        exclude = ('status', 'created_at', 'created_by', 'modified_at', 'modified_by')


class SurveyForm(ModelForm):
    agreement_date = forms.DateField(input_formats = ('%m/%d/%Y',), required=False,
                      widget=forms.DateInput(format = '%m/%d/%Y'))
    contract_start_date = forms.DateField(input_formats = ('%m/%d/%Y',), required=False,
                      widget=forms.DateInput(format = '%m/%d/%Y'))
    # usage_from_date = forms.DateField(input_formats = ('%m/%d/%Y',),
    #                   widget=forms.DateInput(format = '%m/%d/%Y'))
    # usage_to_date = forms.DateField(input_formats = ('%m/%d/%Y',),
    #                   widget=forms.DateInput(format = '%m/%d/%Y'))
    # zone = forms.MultipleChoiceField(choices=settings.ZONE)


    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
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
          # 'service_address_country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}),
          'service_address_zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
          'billing_address_line1': forms.TextInput(attrs={'placeholder': 'Line 1', 'class': 'form-control'}),
          'billing_address_line2': forms.TextInput(attrs={'placeholder': 'Line 2', 'class': 'form-control'}),
          'billing_address_city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
          'billing_address_state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
          # 'billing_address_country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}),
          'billing_address_zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
          'customer_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200 }),
          'utility_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200}),
          'gas_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200 }),
          'electric_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200}),
          'billing_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200}),
          # 'deal_description': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'maxlength': 200}),
          'account_type': forms.RadioSelect(),
          'door_to_door': forms.RadioSelect(),
          'billing': forms.RadioSelect(),
          'commodity_gas': forms.RadioSelect(),
          # 'delivery_type': forms.RadioSelect(),
          # 'gas_price_plan': forms.RadioSelect(),
          'electric': forms.RadioSelect(),
          # 'green': forms.RadioSelect(),
          # 'zone': forms.RadioSelect(),
          # 'electric_price_type': forms.RadioSelect(),
          'therm': forms.RadioSelect(),
          'tax_exempt': forms.RadioSelect(),
          'monthly_budget': forms.RadioSelect(),
          # 'internal_data_available': forms.RadioSelect()
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


class DocForm(ModelForm):
    class Meta:
        model = Doc
        fields = ('survey', 'document')

DocFormSet = inlineformset_factory(Survey, Doc, form=DocForm, extra=1, max_num=3, validate_max=True)