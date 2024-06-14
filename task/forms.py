from django import forms
from task.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('created_date','user_object')
        widgets = {
            "title":forms.TextInput(attrs={'class':'form-control'}),
            "status":forms.Select(attrs={'class':'form-select'}),
            "description":forms.Textarea(attrs={'class':'form-control','rows': 4}),
            "due_date": forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})         
        }
    
    def __init__(self, *args, **kwargs):
        exclude_status = kwargs.pop('exclude_status', False)
        super(TaskForm, self).__init__(*args, **kwargs)
        if exclude_status:
            self.fields.pop('status')

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}), label="Confirm Password")
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        widgets = {
            "username":forms.TextInput(attrs={'class':'form-control'}),
            "email":forms.EmailInput(attrs={'class':'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
