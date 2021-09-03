from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app_users import views

User = get_user_model()


class LoginUserViewTest(TestCase):
    """
    Тестирование представления LoginUserView
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone_number = '123'

    @classmethod
    def setUpTestData(cls):
        user_inst = User(username=cls.username, email=cls.user_email, telephone_number=cls.telephone_number)
        user_inst.set_password(cls.user_password)
        user_inst.save()

    def setUp(self):
        self.auth_url = reverse('app_users:login')

    def test_get_request(self):
        """
        Тестирование GET запроса
        """
        response_get = self.client.get(self.auth_url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_users/login.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_post_request_with_username(self):
        """
        Тестирование POST запроса с использованием username
        """
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)
        response_post = self.client.post(self.auth_url,
                                         {'username': self.username, 'password': self.user_password},
                                         follow=True)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)
        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_post_request_with_user_email(self):
        """
        Тестирование POST запроса с использованием user_email
        """
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)
        response_post = self.client.post(self.auth_url,
                                         {'username': self.user_email, 'password': self.user_password},
                                         follow=True)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)
        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_post_request_with_telephone_number(self):
        """
        Тестирование POST запроса с использованием telephone_number
        """
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)
        response_post = self.client.post(self.auth_url,
                                         {'username': self.telephone_number, 'password': self.user_password},
                                         follow=True)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)
        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_post_request_with_wrong_data(self):
        """
        Тестирование POST запроса
        """
        response_post = self.client.post(self.auth_url,
                                         {'username': 'wrong_username', 'password': 'wrong_password'},
                                         follow=True)
        exception_message = _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ) % {'username': _('username')}

        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'app_users/login.html')
        self.assertFormError(response_post, 'form', None, exception_message)


class LogoutCustomUserViewTest(TestCase):
    """
    Тестирование представления LoginUserView
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'
    telephone_number = '123'

    @classmethod
    def setUpTestData(cls):
        user_inst = User(username=cls.username, email=cls.user_email, telephone_number=cls.telephone_number)
        user_inst.set_password(cls.user_password)
        user_inst.save()

    def setUp(self):
        self.logout_url = reverse('app_users:logout')

    def test_post_request(self):
        """
        Тестирование POST запроса
        """
        self.client.login(username=self.username, password=self.user_password)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)

        response_post = self.client.post(self.logout_url, follow=True)
        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)

    def test_get_request(self):
        """
        Тестирование GET запроса
        """
        self.client.login(username=self.username, password=self.user_password)
        self.assertTrue(self.client.request().wsgi_request.user.is_authenticated)

        response_get = self.client.get(self.logout_url, follow=True)
        self.assertRedirects(response_get, reverse('app_users:user_list'))
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)
        self.assertFalse(self.client.request().wsgi_request.user.is_authenticated)


class RegisterCustomUserViewTest(TestCase):
    """
    Тестирование представления RegisterCustomUserView
    """

    def setUp(self):
        self.register_url = reverse('app_users:register')
        self.request_data = {
            'username': 'test_username',
            'email': 'test@test.ru',
            'telephone_number': '123',
            'password1': '123qweQWE',
            'password2': '123qweQWE',
        }

    def test_get_request(self):
        """
        Тестирование GET запроса
        """

        response_get = self.client.get(self.register_url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_users/register.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.RegisterCustomUserView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса
        """
        response_post = self.client.post(self.register_url, self.request_data, follow=True)

        user = User.objects.get(pk=1)
        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)
        self.assertEqual(user.username, self.request_data['username'])
        self.assertEqual(user.email, self.request_data['email'])
        self.assertEqual(user.telephone_number, f'+{self.request_data["telephone_number"]}')

    def test_post_request_with_strange_telephone_number(self):
        """
        Тестирование POST запроса для проверки корректировки телефонного номера при записи
        """
        good_phone_number = '1234'
        self.request_data['telephone_number'] = f'{good_phone_number}bad_phone_number'

        response_post = self.client.post(self.register_url, self.request_data, follow=True)

        user = User.objects.get(pk=1)
        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)
        self.assertEqual(user.telephone_number, f'+{good_phone_number}')


class DeleteCustomUserViewTest(TestCase):
    """
    Тестирование представления DeleteCustomUserView
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
        self.register_url = reverse('app_users:delete', kwargs={'pk': self.user_inst.id,
                                                                'slug': self.user_inst.slug})

    def test_get_request(self):
        """
        Тестирование GET запроса
        """

        response_get = self.client.get(self.register_url, follow=True)
        self.assertRedirects(response_get, reverse('app_users:user_list'))
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_post_request_another_user_or_not_authenticated_user(self):
        """
        Тестирование POST запроса другим пользователем
        """
        response_post = self.client.post(self.register_url, follow=True)

        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)
        self.assertTrue(User.objects.get(id=1))

    def test_post_request(self):
        """
        Тестирование POST запроса владельцем аккаунта
        """
        self.client.login(username=self.username, password=self.user_password)
        self.assertTrue(User.objects.get(id=1))
        response_post = self.client.post(self.register_url, follow=True)

        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=1)


class CustomUserListViewTest(TestCase):
    """
    Тестирование представления CustomUserListView
    """

    user_count = 100

    @classmethod
    def setUpTestData(cls):
        cls.user_list = []
        for i in range(1, cls.user_count + 1):
            user = User(id=i, username=f'username_{i}', email=f'email@email{i}.ru', telephone_number=f'{i}')
            cls.user_list.append(user)
        User.objects.bulk_create(cls.user_list)

    def setUp(self):
        self.register_url = reverse('app_users:user_list')

    def test_get_request(self):
        """
        Тестирование GET запроса
        """

        response_get = self.client.get(self.register_url)

        users = response_get.context['users']
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(list(users), list(User.objects.all().order_by('username')[:12]))
        self.assertTemplateUsed(response_get, 'app_users/user_list.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_get_request_page_2(self):
        """
        Тестирование GET запроса ко второй странице
        """

        response_get = self.client.get(f'{self.register_url}?page=2')

        users = response_get.context['users']
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(list(users), list(User.objects.all().order_by('username')[12:24]))
        self.assertTemplateUsed(response_get, 'app_users/user_list.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_get_blog_list_with_custom_paginate(self):
        """
        Тестирование GET запроса с установкой пользовательской пагинатора
        """
        users_per_page = 24

        self.client.cookies['users_per_page'] = users_per_page
        response_get = self.client.get(self.register_url)

        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(len(response_get.context['users']), users_per_page)
        self.assertTemplateUsed(response_get, 'app_users/user_list.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_get_blog_list_with_filter_users(self):
        """
        Тестирование GET запроса с установкой фильтра по имени пользователя
        """
        response_get = self.client.get(f"{self.register_url}?username=username_100")

        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(len(response_get.context['users']), 1)
        self.assertTemplateUsed(response_get, 'app_users/user_list.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)


class CustomUserUpdateViewTest(TestCase):
    """
    Тестирование представления CustomUserUpdateView
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
        self.update_url = reverse('app_users:personal_account', kwargs={'pk': self.user_inst.id,
                                                                        'slug': self.user_inst.slug})

    def test_get_request_third_party_user(self):
        """
        Тестирование GET запроса сторонним пользователем
        """

        response_get = self.client.get(self.update_url, follow=True)
        self.assertRedirects(response_get, reverse('app_users:user_list'))
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_get_request(self):
        """
        Тестирование GET запроса владельцем аккаунта
        """
        self.client.login(username=self.username, password=self.user_password)

        response_get = self.client.get(self.update_url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_users/personal_account.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserUpdateView.as_view().__name__)

    def test_post_request_third_party_user(self):
        """
        Тестирование POST запроса сторонним пользователем
        """

        response_get = self.client.post(self.update_url, follow=True)
        self.assertRedirects(response_get, reverse('app_users:user_list'))
        self.assertEqual(response_get.resolver_match.func.__name__, views.CustomUserListView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса владельцем аккаунта
        """
        self.client.login(username=self.username, password=self.user_password)

        user_name = 'new_user_name'
        email = 'new_user_email@email.ru'
        telephone_number = '7777777'
        first_name = 'first_name'
        last_name = 'last_name'

        with open(settings.BASE_DIR / 'project_modules/static/project_modules/images' / 'anonymous-photo.jpg',
                  mode='rb') as image:
            response_post = self.client.post(self.update_url,
                                             {'username': user_name,
                                              'email': email,
                                              'telephone_number': telephone_number,
                                              'first_name': first_name,
                                              'last_name': last_name,
                                              'user_photo': image},
                                             follow=True)
        user = User.objects.get(pk=1)
        uploaded_image_path = settings.BASE_DIR.joinpath(user.user_photo.url.strip('/'))

        self.assertRedirects(response_post, reverse('app_users:personal_account',
                                                    kwargs={'pk': str(user.id), 'slug': user.slug}))
        self.assertTrue(uploaded_image_path.exists())
        uploaded_image_path.unlink()
        self.assertEqual(user.username, user_name)
        self.assertEqual(user.email, email)
        self.assertEqual(user.telephone_number, f'+{telephone_number}')
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserUpdateView.as_view().__name__)


class CustomUserChangePasswordViewTest(TestCase):
    """
    Тестирование представления CustomUserChangePasswordView
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
        self.change_password_url = reverse('app_users:change_password')

    def test_get_request(self):
        """
        Тестирование GET запроса
        """
        self.client.login(username=self.username, password=self.user_password)

        response_get = self.client.get(self.change_password_url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_users/custom_user_password_change.html')
        self.assertEqual(response_get.resolver_match.func.__name__,
                         views.CustomUserChangePasswordView.as_view().__name__)

    def test_get_request_not_auth_user(self):
        """
        Тестирование GET запроса не аутентифицированного пользователя
        """
        response_get = self.client.get(self.change_password_url, follow=True)
        self.assertEqual(response_get.status_code, 200)
        self.assertRedirects(response_get, f"{reverse('app_users:login')}?next={self.change_password_url}")
        self.assertEqual(response_get.resolver_match.func.__name__, views.LoginUserView.as_view().__name__)

    def test_post_request(self):
        """
        Тестирование POST запроса аутентифицированного пользователя
        """
        self.client.login(username=self.username, password=self.user_password)
        new_password = '123rtyUIO'

        response_post = self.client.post(self.change_password_url,
                                         {'old_password': self.user_password,
                                          'new_password1': new_password,
                                          'new_password2': new_password},
                                         follow=True)

        url = reverse('app_users:personal_account', kwargs={'pk': str(self.user_inst.id),
                                                            'slug': self.user_inst.slug})
        self.assertRedirects(response_post, f'{url}?pass_successfully_changed=True')
        self.assertEqual(response_post.resolver_match.func.__name__, views.CustomUserUpdateView.as_view().__name__)
