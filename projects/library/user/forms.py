from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'login__form-input',
            'placeholder': 'Username',
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'login__form-input',
            'placeholder': 'Password',
            'autocomplete': 'off',
        }
    ))


class UserSignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('password1', None)
            self.fields.pop('password2', None)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login__form-input',
        'placeholder': 'Username',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login__form-input',
        'placeholder': 'Password',
        'autocomplete': 'off',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'login__form-input',
        'placeholder': 'Repeat password',
        'autocomplete': 'off',
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login__form-input',
        'placeholder': 'Name',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'login__form-input',
        'placeholder': 'Surname',
    }))
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={
        'class': 'login__form-input',
        'placeholder': 'Email',
    }))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

