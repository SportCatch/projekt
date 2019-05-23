"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import forms
from django.contrib.auth.models import User
from .models import *

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']

class EditProfieForm (forms.ModelForm):
    class Meta:
        model = Profile
        fields = {'photo'}
        labels = {'photo': "Zdjęcie"}

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = {'first_name', 'last_name','email','username'}

class ContactForm(forms.Form):
    subject = forms.CharField(required = True,widget=forms.TextInput(attrs={'size': 60}))
    message = forms.CharField(widget = forms.Textarea(attrs={'rows':18,
                                            'cols':70,
                                            'style':'resize:none;'}))
