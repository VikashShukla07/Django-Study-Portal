from django.forms import widgets
from django import forms
from .models import Notes,Homework,User
from django.contrib.auth.forms import UserCreationForm
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes

        fields=['title', 'description']

class DateInput(forms.DateInput):
    input_type = 'date'

    
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due_date':DateInput()}
        fields=['Subject','title', 'description','due_date','is_finished']

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=30,label="Enter Your Search")


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model= User
        fields =['username','email','password1', 'password1']