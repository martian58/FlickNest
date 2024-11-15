# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'Email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'Last Name'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 bg-gray-800 text-gray-200 border border-gray-700 rounded-md focus:outline-none focus:border-blue-500',
            'placeholder': 'Password'
        })
    )
