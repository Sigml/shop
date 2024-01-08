from django import forms
from django.forms import TextInput, CharField, PasswordInput, EmailField, ImageField, DateInput, IntegerField, DateField
from .models import CustomUser


class UserCreationForm(forms.ModelForm):
    password_confirmation = CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'hasło'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_confirmation', 'first_name', 'last_name')
        widgets = {

            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'email'

            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'haslo'
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'imię'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nazwisko'
            })

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError('Podane hasła różnią się')

        return cleaned_data
    

class LoginForm(forms.Form):
    email = CharField(label='email', widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'email'
    }))

    password = CharField(label='password', widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'hasło'
    }))


class SeachUserForm(forms.Form):
    email = CharField(label='email', widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'email'
    }))


class ResetPasswordForm(forms.Form):
    password = CharField(label='password', widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'hasło'
    }))
    password_confirmation = CharField(label='Password confirmation', widget=PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'hasło'
    }))


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'number_phone', 'date_of_birth', 'description']
        widgets = {
    'username' : TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }),
    
    'email' :TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }),
    
    'first_name': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Imię'
    }),
    'last_name':TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nazwiśko'
    }),
    'number_phone': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Numer telefonu'
    }),
    'date_of_birth': DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Data urodzenia'
    }),
    'description': TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'O sobię'
    })
    }