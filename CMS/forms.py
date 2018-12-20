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
          'customer_type': forms.RadioSelect(),
          'billing': forms.RadioSelect(),
        }
        fieldsets = (
            ("Contract Information", {
                'fields': ('survey_completed_by', 'agreement_date', 'account_type'),
            }),
            ("Customer & Billing Information", {
                'fields': ('customer_name', 'completed_by', 'service_address','billing_address', 'customer_phone',\
                           'customer_email', 'sbc', 'salesperson_name', 'door_to_door','customer_type', 'billing'),
            }),
        )
