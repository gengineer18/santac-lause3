from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Present
import re


def isalnumsym(value):
    return re.match(r'^[a-zA-Z0-9_@.+-]+$', value) is not None


class SignupForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not isalnumsym(username):
            raise forms.ValidationError("半角アルファベット、半角数字、@/./+/-/_ で入力してください")
        return username


class ProfileEditForm(forms.Form):

    introduce = forms.CharField(
        label='自己紹介:',
        max_length=400,
        required=False,
        help_text='400字以内で入力してください'
    )

    location = forms.CharField(
        label='場所:',
        max_length=30,
        required=False,
        help_text='30字以内で入力してください'
    )

    web_site = forms.CharField(
        label='Webサイト:',
        max_length=2100,
        required=False
    )

    icon = forms.ImageField(
        label='アイコン:',
        required=False,
        widget=forms.FileInput
    )


class PresentForm(forms.ModelForm):
    class Meta:
        model = Present
        fields = (
            'title',
            'conclusion',
            'topic1',
            'image1',
            'contents1',
            'topic2',
            'image2',
            'contents2',
            'topic3',
            'image3',
            'contents3',
        )
        widgets = {
            'conclusion': forms.Textarea(attrs={'cols': 40, 'rows': 7}),
            'contents1': forms.Textarea(attrs={'rows': 7}),
            'contents2': forms.Textarea(attrs={'rows': 7}),
            'contents3': forms.Textarea(attrs={'rows': 7}),
            'image1': forms.FileInput,
            'image2': forms.FileInput,
            'image3': forms.FileInput
        }


class AccountEditForm(forms.ModelForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not isalnumsym(username):
            raise ValidationError("半角アルファベット、半角数字、@/./+/-/_ で入力してください")
        return username
