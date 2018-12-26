from django import forms
from django.forms import ModelForm

from CMS.models import *


class SurveyForm(ModelForm):

    class Meta:
        model = Survey
        exclude = ('created_at',)
        widgets = {
          'survey_completed_by': forms.TextInput(attrs={'placeholder': 'First Name, Last Name'}),
          'customer_name': forms.TextInput(attrs={'placeholder': 'First Name, Last Name'}),
          'completed_by': forms.TextInput(attrs={'placeholder': 'First Name, Last Name'}),
          'salesperson_name': forms.TextInput(attrs={'placeholder': 'First Name, Last Name'}),
          'account_type': forms.RadioSelect(),
          'sbc': forms.RadioSelect(),
          # 'customer_type': forms.RadioSelect(),
          'door_to_door': forms.RadioSelect(),
          'billing': forms.RadioSelect(),
          # 'passthru': forms.RadioSelect(),
          # 'rate_class': forms.RadioSelect(),
          # 'gas_rate_class': forms.RadioSelect(),
          # 'electric_utility': forms.RadioSelect(),
          # 'gas_utility': forms.RadioSelect(),
          # 'utility_account_type': forms.RadioSelect(),
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

