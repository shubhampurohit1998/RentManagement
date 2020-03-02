import datetime
from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from . models import *
from django.forms import ModelForm, Textarea
from allauth.account.forms import SignupForm


class DateInput(forms.DateInput):
    input_type = 'date'


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
        if not first_name.isalpha():
            raise forms.ValidationError('Name can not contains digits')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError('Surname can not contains digits')
        return last_name

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

        def clean_size(self):
            size = self.cleaned_data['size']
            if len(size) < 4:
                raise forms.ValidationError('Size should 4 characters long')
            return size


class InsertImageForm(ModelForm):

    class Meta:
        model = Picture
        fields = '__all__'
        widgets = {'property': forms.HiddenInput(), 'pic_name': forms.FileInput()}
        labels = {
            'pic_name': 'Select image'
        }


class RentForm(ModelForm):
    # date_on_rent = forms.DateField()
    # period = forms.DateField

    class Meta:
        model = Rent
        fields = "__all__"
        widgets = {'property': forms.HiddenInput(),
                   'customer': forms.HiddenInput(),
                   'request_accept': forms.HiddenInput(),
                   'is_active': forms.HiddenInput(),
                   'date_on_rent': forms.TextInput(attrs={'readonly': 'readonly'}),
                   'tenure': DateInput(),
                   }

    def clean_tenure(self):
        tenure = self.cleaned_data['tenure']
        if tenure is None or tenure <= datetime.date.today():
            raise ValidationError("Tenure date is not valid")
        return tenure


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, label='',   widget=forms.TextInput
                            (attrs={'placeholder': 'search here', }), required=False)


class UpdateProfileUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'gender', 'profile_picture', ]

        def clean_mobile(self):
            mobile = self.cleaned_data['mobile']
            if not str.isdigit(mobile):
                raise forms.ValidationError('Mobile number can not be in characters')
            return self.cleaned_data['mobile']

        def clean_first_name(self):
            first_name = self.cleaned_data['first_name']
            if not first_name.isalpha():
                raise forms.ValidationError('Name can not contains digits')
            return first_name

        def clean_last_name(self):
            last_name = self.cleaned_data['last_name']
            if not last_name.isalpha():
                raise forms.ValidationError('Surname can not contains digits')
            return last_name


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
            'message': forms.Textarea(attrs={'cols': 35, 'rows': 2}),
            'rent': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'receiver': forms.HiddenInput(),
        }

        def clean_message(self):
            # import pdb;
            # pdb.set_trace()
            message = self.cleaned_data['message']
            if message is None:
                raise ValidationError('Empty message')
            return message


class LeaveRequestForm(ModelForm):

    class Meta:
        model = LeaveRequest
        fields = '__all__'
        widgets = {
            'rent': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'request_accept': forms.HiddenInput(),
        }
