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

