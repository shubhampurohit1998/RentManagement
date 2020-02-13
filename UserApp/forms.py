from django import forms
from . models import *
from django.forms import ModelForm
from allauth.account.forms import SignupForm
from allauth.account.forms import LoginForm


class RegisterForm(SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Person
        fields = ['__all__']

    mobile = forms.CharField(max_length=10)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    def save(self, request):
        user = super(RegisterForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        # user.mobile = self.cleaned_data['mobile']
        # user.gender = self.cleaned_data['gender']
        p = Person(mobile=self.cleaned_data['mobile'], gender=self.cleaned_data['gender'], user=user)
        p.save()

        return user


