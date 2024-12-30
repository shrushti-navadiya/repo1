from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Answer, User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'selected_option']
