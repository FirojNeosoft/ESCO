from django import forms
from django.forms import ModelForm

from CMS.models import *


class SurveyForm(ModelForm):
    agreement_date = forms.DateField(input_formats = ('%m/%d/%Y',),
                      widget=forms.DateInput(format = '%m/%d/%Y'))
    contract_start_date = forms.DateField(input_formats = ('%m/%d/%Y',),
                      widget=forms.DateInput(format = '%m/%d/%Y'))
    usage_from_date = forms.DateField(input_formats = ('%m/%d/%Y',),
                      widget=forms.DateInput(format = '%m/%d/%Y'))
    usage_to_date = forms.DateField(input_formats = ('%m/%d/%Y',),
                      widget=forms.DateInput(format = '%m/%d/%Y'))
    class Meta:
        model = Survey
        exclude = ('created_at',)
        widgets = {
          'service_address_line1': forms.TextInput(attrs={'placeholder': 'Line 1', 'class': 'form-control'}),
          'service_address_line2': forms.TextInput(attrs={'placeholder': 'Line 2', 'class': 'form-control'}),
          'service_address_city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
          'service_address_state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
          'service_address_country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}),
          'service_address_zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
          'billing_address_line1': forms.TextInput(attrs={'placeholder': 'Line 1', 'class': 'form-control'}),
          'billing_address_line2': forms.TextInput(attrs={'placeholder': 'Line 2', 'class': 'form-control'}),
          'billing_address_city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}),
          'billing_address_state': forms.TextInput(attrs={'placeholder': 'State', 'class': 'form-control'}),
          'billing_address_country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-control'}),
          'billing_address_zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code', 'class': 'form-control'}),
          'account_type': forms.RadioSelect(),
          'sbc': forms.RadioSelect(),
          'door_to_door': forms.RadioSelect(),
          'billing': forms.RadioSelect(),
          'commodity_gas': forms.RadioSelect(),
          'delivery_type': forms.RadioSelect(),
          'gas_price_plan': forms.RadioSelect(),
          'electric': forms.RadioSelect(),
          'green': forms.RadioSelect(),
          'Zone': forms.RadioSelect(),
          'electric_price_type': forms.RadioSelect(),
          'therm': forms.RadioSelect(),
          'tax_exempt': forms.RadioSelect(),
          'monthly_budget': forms.RadioSelect(),
          'internal_data_available': forms.RadioSelect()
        }


