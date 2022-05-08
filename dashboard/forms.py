from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class NotesForm(forms.ModelForm):
    class Meta:
        model=Notes
        fields=["Title", "Description"]

class DateInput(forms.DateInput):
    input_type = 'date'

class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        widgets = {'due' : DateInput() }
        fields=["subject","title","description","due","status"]


class DashBoardForm(forms.Form):
    text = forms.CharField(max_length=200, label="Enter your Search: ")

class TodoForm(forms.ModelForm):
    class Meta:
        model=ToDo
        fields=['title','status']

class ConversionForm(forms.Form):
    CHOICES = [('length','Length'),('mass','Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICES=[('yard','Yard'),('foot','Foot')]
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'type':'number','placeholder':'Enter the number'})
    )
    measure1=forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICES)
     )
    measure2 = forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICES)
    )

class ConversionMassForm(forms.Form):
    CHOICES = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'type': 'number','placeholder':'Enter the number'})
    )
    measure1 = forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICES)
    )
    measure2 = forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICES)
    )

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'password1', 'password2']




