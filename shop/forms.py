from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from .models import CustomUser
from .utils.constant import REGEX

class SignUpForm(UserCreationForm):
    phone_regex = RegexValidator(REGEX, message=_('Wrong phone number format!'))
    phone = forms.CharField(validators=[phone_regex], max_length=17, label=_('Phone'))
    username = forms.CharField(required=True, max_length=30, label=_('Username'))
    first_name = forms.CharField(required=True, max_length=30, label=_('First name'))
    last_name = forms.CharField(required=True, max_length=30, label=_('Last name'))
    address = forms.CharField(required=True, max_length=30, label=_('Address'))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput, label=_('Password'))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput, label=_('Confirm password'))
    email = forms.EmailField(required=True, label=_('Email'), widget=forms.EmailInput)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'address', 'password1', 'password2')
