"""
Accounts forms — Registration and login forms.
Naming Convention:
  - Class names: PascalCase ending with 'Form'
  - Method names: snake_case starting with 'clean_'
  - Variables: snake_case
"""

import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

# Password rule constants — SCREAMING_SNAKE_CASE
MAX_PASSWORD_LENGTH = 15
MIN_PASSWORD_LENGTH = 8
PASSWORD_PATTERN    = r'[!@#$%^&*(),.?":{}|<>_\-]'


class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering new users.
    PascalCase class name, ends with 'Form'.
    """

    # snake_case field names
    password_input   = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Enter password',
            'maxlength':   str(MAX_PASSWORD_LENGTH),
            'id':          'id-password-input',
        })
    )
    password_confirm = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Confirm your password',
            'maxlength':   str(MAX_PASSWORD_LENGTH),
            'id':          'id-password-confirm',
        })
    )

    class Meta:
        model  = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'role',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'First Name',
                'id':          'id-first-name',
            }),
            'last_name': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Last Name',
                'id':          'id-last-name',
            }),
            'username': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Username',
                'id':          'id-username',
            }),
            'email': forms.EmailInput(attrs={
                'class':       'form-control',
                'placeholder': 'Email Address',
                'id':          'id-email',
            }),
            'phone': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Phone Number',
                'id':          'id-phone',
            }),
            'role': forms.Select(attrs={
                'class': 'form-select',
                'id':    'id-role',
            }),
        }

    # snake_case clean methods — Django convention
    def clean_first_name(self):
        """Capitalize first letter of first name."""
        first_name = self.cleaned_data.get('first_name', '')
        return first_name.capitalize()

    def clean_last_name(self):
        """Capitalize first letter of last name."""
        last_name = self.cleaned_data.get('last_name', '')
        return last_name.capitalize()

    def clean_password_input(self):
        """Validate password against all rules."""
        password = self.cleaned_data.get('password_input', '')

        # Check max length
        if len(password) > MAX_PASSWORD_LENGTH:
            raise ValidationError(
                f'Password must be maximum {MAX_PASSWORD_LENGTH} characters.'
            )

        # Check min length
        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f'Password must be at least {MIN_PASSWORD_LENGTH} characters.'
            )

        # Check uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                'Password must contain at least one uppercase letter (A-Z).'
            )

        # Check lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                'Password must contain at least one lowercase letter (a-z).'
            )

        # Check number
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                'Password must contain at least one number (0-9).'
            )

        # Check special character
        if not re.search(PASSWORD_PATTERN, password):
            raise ValidationError(
                'Password must contain at least one special character (!@#$%^&*).'
            )

        return password

    def clean_password_confirm(self):
        """Check that both passwords match."""
        password_input   = self.cleaned_data.get('password_input')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password_input and password_confirm:
            if password_input != password_confirm:
                raise ValidationError('Passwords do not match.')

        return password_confirm

    def save(self, commit=True):
        """Save user with hashed password."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_input'])
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Form for user login.
    PascalCase class name, ends with 'Form'.
    """

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':       'form-control',
            'placeholder': 'Enter username',
            'id':          'id-login-username',
            'autofocus':   True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Enter password',
            'id':          'id-login-password',
        })
    )