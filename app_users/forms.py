import re

from django.contrib.auth.password_validation import password_validators_help_texts
from django.forms import ModelForm, TextInput, CharField, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField, \
    PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from app_users import models
from app_users.widgets import CustomClearableFileInput
from project_modules.forms import ChangeIsValidFormMixin


PASSWORD_HELP_TEXT = _("Your password can’t be too similar to your other personal information.Your password must "
                       "contain at least 8 characters.Your password can’t be a commonly used password.Your password "
                       "can’t be entirely numeric.")
FIELDS_HELP_TEXT_AND_ATTRIBUTES = {
    'username': {
        'help_text': '',
        'attributes': {'placeholder': _('Login'),
                       'aria-label': _('Enter your username'), },
    },
    'email': {
        'help_text': _('The email address must contain "@"'),
        'attributes': {'placeholder': 'E-mail',
                       'aria-label': _('Enter your e-mail'), },
    },
    'telephone_number': {
        'help_text': _('Enter your phone number'),
        'attributes': {'placeholder': _('Phone number'),
                       'type': 'tel',
                       'aria-label': _('Enter your phone number'),
                       'data-tel-input': True, },
    },
    'first_name': {
        'help_text': _('Enter your first name'),
        'attributes': {'placeholder': _('Enter your first name'),
                       'aria-label': _('Enter your first name'), },
    },
    'last_name': {
        'help_text': _('Enter your surname'),
        'attributes': {'placeholder': _('Enter your surname'),
                       'aria-label': _('Enter your surname'), },
    },
    'user_photo': {
        'help_text': _('Select your photo'),
        'attributes': {'placeholder': '',
                       'aria-label': '', },
    },
    'password1': {
        'help_text': PASSWORD_HELP_TEXT,
        'attributes': {'placeholder': _('Enter password'),
                       'aria-label': _('Enter password'), },
    },
    'password2': {
        'help_text': _('Repeat the password'),
        'attributes': {'placeholder': _('Repeat the password'),
                       'aria-label': _('Repeat the password'), },
    },
    'old_password': {
        'help_text': _('Enter your old password'),
        'attributes': {'placeholder': _('Enter your old password'),
                       'aria-label': _('Enter your old password'), },
    },
    'new_password1': {
        'help_text': PASSWORD_HELP_TEXT,
        'attributes': {'placeholder': _('Enter new password'),
                       'aria-label': _('Enter new password'), },
    },
    'new_password2': {
        'help_text': _('Repeat the password'),
        'attributes': {'placeholder': _('Repeat the password'),
                       'aria-label': _('Repeat the password'), },
    },
}

LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME = 'login-register-update__field'


class CleanedUserProfileTelephoneMixin:
    """
    Миксин для проверки поля telephone_number модели CustomUser.
    """

    def clean_telephone_number(self):
        telephone = self.cleaned_data['telephone_number']
        telephone_digits = re.sub(r'\D', '', telephone)

        if telephone.startswith('8'):
            telephone = f'+7{telephone_digits[1:]}'
        else:
            telephone = f'+{telephone_digits}'

        return telephone


class AuthForm(AuthenticationForm, ChangeIsValidFormMixin):
    """
    Форма аутентификации пользователя.
    """
    username = UsernameField(
        widget=TextInput(attrs={
            'autofocus': True,
            'placeholder': _('Enter username, e-mail or phone number'),
            'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME,
        }),
    )
    password = CharField(
        strip=False,
        widget=PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': _('Enter password'),
            'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME,
        }),
    )


class CustomUserChangeForm(ModelForm, CleanedUserProfileTelephoneMixin, ChangeIsValidFormMixin):
    """
    Форма для редактирования пользователя через сайт.
    """

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

        for field_name in ['email', 'telephone_number', 'first_name', 'last_name']:
            self.fields[field_name].help_text = FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['help_text']

        for field in self.fields.values():
            field.widget.attrs.update({'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME,
                                       'title': f'{field.help_text}', })

        for field_name in ['username', 'email', 'telephone_number', 'first_name', 'last_name']:
            self.fields[field_name].widget.attrs.update(FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['attributes'])

    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'telephone_number', 'first_name', 'last_name', 'user_photo')
        widgets = {
            'user_photo': CustomClearableFileInput(),
        }


class UserChangePasswordForm(PasswordChangeForm, ChangeIsValidFormMixin):
    """
    Форма смены пароля пользователя.
    """

    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].help_text = FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['help_text']

        for field in self.fields.values():
            field.widget.attrs.update({'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME,
                                       'title': f'{field.help_text}', })

        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].widget.attrs.update(FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['attributes'])


class CustomUserCreationForm(UserCreationForm, CleanedUserProfileTelephoneMixin, ChangeIsValidFormMixin):
    """
    Форма для создания нового пользователя, включает все обязательные поля и два поля для пароля.
    """

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name in ['email', 'telephone_number', 'password1', 'password2']:
            self.fields[field_name].help_text = FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['help_text']

        for field in self.fields.values():
            field.widget.attrs.update({'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME,
                                       'title': f'{field.help_text}', })

        for field_name in ['username', 'email', 'telephone_number', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.update(FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['attributes'])

    class Meta(UserCreationForm.Meta):
        model = models.CustomUser
        fields = ('username', 'email', 'telephone_number')


class AdminCustomUserChangeForm(UserChangeForm, CleanedUserProfileTelephoneMixin, ChangeIsValidFormMixin):
    """
    Форма для редактирования пользователя в админке.
    """

    class Meta(UserChangeForm.Meta):
        model = models.CustomUser
