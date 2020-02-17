from django import forms
from . models import *
from django.forms import ModelForm, Textarea
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


class PropertyRegisterForm(ModelForm):

    class Meta:
        model = Property
        # fields = ['price', 'size', 'address', 'p_type', 'city']
        fields = '__all__'
        widgets = {'owner': forms.HiddenInput(), 'address': Textarea(attrs={'cols': 40, 'rows': 3})}
        labels = {
            'p_type': 'Property type',
            # 'owner': forms.HiddenInput()
        }
        help_texts = {
            'Property type': 'Select which kind of property you wanna add here.....',
        }


class InsertImageForm(ModelForm):

    class Meta:
        model = Picture
        fields = '__all__'
        widgets = {'property': forms.HiddenInput(), 'pic_name': forms.FileInput()}
        labels = {
            'pic_name': 'Select image'
        }