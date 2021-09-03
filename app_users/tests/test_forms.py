from django.contrib.auth import get_user_model
from django.test import TestCase

from app_users import forms
from app_users.widgets import CustomClearableFileInput

User = get_user_model()


class BlogFormTest(TestCase):
    """
    Тестирование формы BlogForm
    """

    def setUp(self):
        self.form = forms.AuthForm()

    def test_username_field_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля username
        """
        self.assertEqual(self.form.fields['username'].widget.attrs['class'],
                         forms.LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME)

    def test_password_field_widget_attrs(self):
        """
        Тестирование атрибутов widget у поля password
        """
        self.assertEqual(self.form.fields['password'].widget.attrs['class'],
                         forms.LOGIN_REGISTER_UPDATE_FIELD_CLASS_NAME)


class CustomUserChangeFormTest(TestCase):
    """
    Тестирование формы CustomUserChangeForm
    """

    def setUp(self):
        self.form = forms.CustomUserChangeForm()

    def test_email_field_help_text(self):
        """
        Тестирование help_text у поля email
        """
        self.assertEqual(self.form.fields['email'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['email']['help_text'])

    def test_telephone_number_field_help_text(self):
        """
        Тестирование help_text у поля telephone_number
        """
        self.assertEqual(self.form.fields['telephone_number'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['telephone_number']['help_text'])

    def test_first_name_field_help_text(self):
        """
        Тестирование help_text у поля first_name
        """
        self.assertEqual(self.form.fields['first_name'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['first_name']['help_text'])

    def test_last_name_field_help_text(self):
        """
        Тестирование help_text у поля last_name
        """
        self.assertEqual(self.form.fields['last_name'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['last_name']['help_text'])

    def test_username_field_widget(self):
        """
        Тестирование widget у поля user_photo
        """
        self.assertTrue(isinstance(self.form.fields['user_photo'].widget, CustomClearableFileInput))

    def test_telephone_number_field_is_valid_1(self):
        """
        Тестирование валидации у поля telephone_number начинающегося с любой цифры кроме 8
        """
        telephone_number = '123'
        form = forms.CustomUserChangeForm(data={'telephone_number': telephone_number})
        form.full_clean()
        self.assertEqual(form.cleaned_data['telephone_number'], f'+{telephone_number}')

    def test_telephone_number_field_is_valid_3(self):
        """
        Тестирование валидации у поля telephone_number начинающегося с 8
        """
        telephone_number = '823'
        form = forms.CustomUserChangeForm(data={'telephone_number': telephone_number})
        form.full_clean()
        self.assertEqual(form.cleaned_data['telephone_number'], f'+7{telephone_number[1:]}')


class UserChangePasswordFormTest(TestCase):
    """
    Тестирование формы UserChangePasswordForm
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone_number = '123'

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User(username=cls.username, email=cls.user_email, telephone_number=cls.telephone_number)
        cls.user_inst.set_password(cls.user_password)
        cls.user_inst.save()

    def setUp(self):
        self.form = forms.UserChangePasswordForm(user=self.user_inst)

    def test_old_password_field_help_text(self):
        """
        Тестирование help_text у поля old_password
        """
        self.assertEqual(self.form.fields['old_password'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['old_password']['help_text'])

    def test_new_password1_field_help_text(self):
        """
        Тестирование help_text у поля new_password1
        """
        self.assertEqual(self.form.fields['new_password1'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['new_password1']['help_text'])

    def test_new_password2_field_help_text(self):
        """
        Тестирование help_text у поля new_password2
        """
        self.assertEqual(self.form.fields['new_password2'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['new_password2']['help_text'])


class CustomUserCreationFormTest(TestCase):
    """
    Тестирование формы CustomUserCreationForm
    """
    def setUp(self):
        self.form = forms.CustomUserCreationForm()

    def test_email_field_help_text(self):
        """
        Тестирование help_text у поля email
        """
        self.assertEqual(self.form.fields['email'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['email']['help_text'])

    def test_telephone_number_field_help_text(self):
        """
        Тестирование help_text у поля telephone_number
        """
        self.assertEqual(self.form.fields['telephone_number'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['telephone_number']['help_text'])

    def test_password1_field_help_text(self):
        """
        Тестирование help_text у поля password1
        """
        self.assertEqual(self.form.fields['password1'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['password1']['help_text'])

    def test_password2_field_help_text(self):
        """
        Тестирование help_text у поля password2
        """
        self.assertEqual(self.form.fields['password2'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['password2']['help_text'])
