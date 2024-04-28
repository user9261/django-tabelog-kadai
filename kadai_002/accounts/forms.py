# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserBaseForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'postal_code', 'address', 'phone_number']


class SignUpForm(UserCreationForm, UserBaseForm):
    class Meta(UserBaseForm.Meta):
        fields = ['account_id'] + UserBaseForm.Meta.fields


class UserEditForm(UserBaseForm):
    pass

