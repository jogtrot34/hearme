from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            "class": "form-control",
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            "class": "form-control",
            'name': 'username',
            'required': '',

        })
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your first name',
            "class": "form-control",
            'name': 'first_name',
            'required': '',

        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your last name',
            "class": "form-control",
            'name': 'last_name',
            'required': '',
    })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Set your new password',
            "class": "form-control",
            'name': 'password1',
            'required': '',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            "class": "form-control",
            'name': 'password2',
            'required': '',

        })
    )

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            "class": "form-control",
            'name': 'username',
            'required': '',

        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'form-control',
            'name': 'username',
            'required': '',

        })
    )
