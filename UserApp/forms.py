from django import forms
from django.contrib.auth.models import Group
from . models import *
from django.forms import ModelForm, Textarea
from allauth.account.forms import SignupForm


class RegisterForm(SignupForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    mobile = forms.CharField(max_length=10)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    USER_TYPE_CHOICE = (
        ('o', 'Owner'),
        ('c', 'Customer')
    )
    are_you = forms.ChoiceField(choices=USER_TYPE_CHOICE)

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not str.isdigit(mobile):
            raise forms.ValidationError('Mobile number can not be in characters')
        return self.cleaned_data['mobile']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not str.isalpha(first_name):
            raise forms.ValidationError('Name can not contains digits')
        return self.cleaned_data[first_name]

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not str.isalpha(last_name):
            raise forms.ValidationError('Surname can not contains digits')
        return self.cleaned_data[last_name]

    def save(self, request):
        user = super(RegisterForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.mobile = self.cleaned_data['mobile']
        user.gender = self.cleaned_data['gender']
        if request.POST['are_you'] == 'o':
            group = Group.objects.get(name='owner')
            group.user_set.add(user)
            user.is_owner = True
        elif request.POST['are_you'] == 'c':
            group = Group.objects.get(name='customer')
            group.user_set.add(user)
            user.is_customer = True
        user.save()
        return user


class PropertyRegisterForm(ModelForm):

    class Meta:
        model = Property
        # fields = ['price', 'size', 'address', 'p_type', 'city']
        fields = '__all__'
        widgets = {'owner': forms.HiddenInput(),
                   'is_active': forms.HiddenInput(),
                   'address': Textarea(attrs={'cols': 40, 'rows': 2}),
                   'description': Textarea(attrs={'cols': 40, 'rows': 2}),
                   }
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


class RentForm(ModelForm):

    class Meta:
        model = Rent
        fields = "__all__"
        widgets = {'property': forms.HiddenInput(),
                   'customer': forms.HiddenInput(),
                   'request_accept': forms.HiddenInput(),
                   'date_on_rent': forms.DateInput,
                   'tenure': forms.DateInput,
                   }

    # def __init__(self, *args, **kwargs):
    #     super(RentForm, self).__init__(*args, **kwargs)
    #     self.fields['date_on_rent'].disabled = True


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, label='',   widget=forms.TextInput
                            (attrs={'placeholder': 'search here', }), required=False)
    # widgets = {
    #     'query': forms.Form
    # }


class UpdateProfileUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'gender', 'profile_picture', ]


# class DemoPersonForm(ModelForm):
#
#     class Meta:
#         model = Person
#         fields = '__all__'
#
#     widgets = {
#         'user': forms.HiddenInput()
#     }
#
#
# class DemoUserForm(ModelForm):
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name']

class ProfilePictureForm(ModelForm):
    class Meta:
        model = User
        # fields = ['profile_picture']
        fields = '__all__'


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'rent': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }


class LeaveRequestForm(ModelForm):

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        widgets = {
            'rent': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'request_accept': forms.HiddenInput(),
        }