import re

from django.contrib.auth.password_validation import password_validators_help_texts
from django.forms import ModelForm, TextInput, CharField, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField, \
    PasswordChangeForm

from app_users import models
from app_users.widgets import CustomClearableFileInput
from project_modules.forms import ChangeIsValidFormMixin

FIELDS_HELP_TEXT_AND_ATTRIBUTES = {
    'username': {
        'help_text': '',
        'attributes': {'placeholder': 'Логин',
                       'aria-label': 'Введите ваш логин', },
    },
    'email': {
        'help_text': 'Адрес электронной почты должен содержать "@"',
        'attributes': {'placeholder': 'E-mail',
                       'aria-label': 'Введите ваш e-mail', },
    },
    'telephone_number': {
        'help_text': 'Введите ваш номер телефона',
        'attributes': {'placeholder': 'Номер телефона',
                       'type': 'tel',
                       'aria-label': 'Введите ваш номер телефона',
                       'data-tel-input': True, },
    },
    'first_name': {
        'help_text': 'Введите ваше имя',
        'attributes': {'placeholder': 'Введите имя',
                       'aria-label': 'Введите имя', },
    },
    'last_name': {
        'help_text': 'Введите вашу фамилию',
        'attributes': {'placeholder': 'Введите фамилию',
                       'aria-label': 'Введите фамилию', },
    },
    'user_photo': {
        'help_text': 'Выберите вашу фотографию',
        'attributes': {'placeholder': '',
                       'aria-label': '', },
    },
    'password1': {
        'help_text': ''.join(password_validators_help_texts()),
        'attributes': {'placeholder': 'Введите пароль',
                       'aria-label': 'Введите пароль', },
    },
    'password2': {
        'help_text': 'Повторите пароль',
        'attributes': {'placeholder': 'Повторите пароль',
                       'aria-label': 'Повторите пароль', },
    },
    'old_password': {
        'help_text': 'Введите ваш старый пароль',
        'attributes': {'placeholder': 'Введите старый пароль',
                       'aria-label': 'Введите старый пароль', },
    },
    'new_password1': {
        'help_text': ''.join(password_validators_help_texts()),
        'attributes': {'placeholder': 'Введите новый пароль',
                       'aria-label': 'Введите новый пароль', },
    },
    'new_password2': {
        'help_text': 'Повторите пароль',
        'attributes': {'placeholder': 'Повторите пароль',
                       'aria-label': 'Повторите пароль', },
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
            'placeholder': 'Введите логин, e-mail или телефон',
            'class': LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME,
        }),
    )
    password = CharField(
        strip=False,
        widget=PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Введите пароль',
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
