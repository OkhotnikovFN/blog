from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.test import TestCase

User = get_user_model()


class CustomUserModelTest(TestCase):
    """
    Тестирование модели Blog
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        user_inst = User(username=cls.username, email=cls.user_email)
        user_inst.set_password(cls.user_password)
        user_inst.save()

    def test_email_field_label(self):
        """
        Тестирование verbose_name у поля email
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, _('email address'))

    def test_telephone_number_field_label(self):
        """
        Тестирование verbose_name у поля telephone_number
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('telephone_number').verbose_name
        self.assertEquals(field_label, _('telephone number'))

    def test_user_photo_field_label(self):
        """
        Тестирование verbose_name у поля user_photo
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('user_photo').verbose_name
        self.assertEquals(field_label, _('profile photo'))

    def test_slug_field_label(self):
        """
        Тестирование verbose_name у поля slug
        """
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug-url')

    def test_telephone_number_field_max_length(self):
        """
        Тестирование max_length у поля telephone_number
        """
        user = User.objects.get(id=1)
        field_max_length = user._meta.get_field('telephone_number').max_length
        self.assertEquals(field_max_length, 20)

    def test_get_absolute_url(self):
        """
        Тестирование метода get_absolute_url
        """
        user = User.objects.get(id=1)
        self.assertEquals(user.get_absolute_url(),
                          reverse('app_users:personal_account', kwargs={'pk': 1, 'slug': user.slug}))
