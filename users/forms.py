from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text='Enter a strong password.')
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                help_text='Enter the same password again for verification.')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        help_texts = {
            'email': None,
            'password': None,
            'password2': None,
        }


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class VerificationForm(forms.Form):
    verification_code = forms.CharField(label='Verification Code', max_length=6)

