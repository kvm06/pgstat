from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.forms.models import ModelForm
from django.utils.regex_helper import Choice
from .models import StatementDetailsView, PERIOD_CHOICES

class FilterForm(forms.Form):
    group_dbs = forms.BooleanField(label="Базам данных", required=False,
                                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    group_users = forms.BooleanField(label="Пользователям", required=False,
                                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    group_levels = forms.BooleanField(label="Уровням", required=False,
                                                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    period = forms.ChoiceField(label="Периоду", choices=PERIOD_CHOICES, initial={"period": "minute"})

