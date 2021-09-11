import datetime
import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from app_blog import models, views
from app_users.views import LoginUserView, CustomUserListView

User = get_user_model()


class CreateBlogViewTest(TestCase):
    """
    Тестирование представления CreateBlogView
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        user_inst = User(username=cls.username, email=cls.user_email)
        user_inst.set_password(cls.user_password)
        user_inst.save()

    def setUp(self):
        self.create_blog_url = reverse('app_blog:blog_create')
        self.auth_url = reverse("app_users:login")

    def test_get_create_blog_not_auth_user(self):
        """
        Тестирование GET запроса неаутентифицированного пользователя
        """
        response_get = self.client.get(self.create_blog_url, follow=True)
        self.assertRedirects(response_get, f'{self.auth_url}?next={self.create_blog_url}')
        self.assertEqual(response_get.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_create_blog_auth_user(self):
        """
        Тестирование GET запроса аутентифицированного пользователя
        """
        self.client.login(username=self.username, password=self.user_password)

        response_get = self.client.get(self.create_blog_url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_blog/create_blog.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.CreateBlogView.as_view().__name__)

    def test_post_create_blog_not_auth_user(self):
        """
        Тестирование POST запроса неаутентифицированного пользователя
        """
        response_post = self.client.post(self.create_blog_url, {'text': 'test text'}, follow=True)
        self.assertRedirects(response_post, f'{self.auth_url}?next={self.create_blog_url}')
        self.assertEqual(response_post.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_post_create_blog_auth_user_with_wrong_data(self):
        """
        Тестирование POST запроса аутентифицированного пользователя, при вводе в форму неверных данных
        """
        self.client.login(username=self.username, password=self.user_password)

        response_post = self.client.post(self.create_blog_url, {'text': ''})
        self.assertEqual(response_post.status_code, 200)
        self.assertFormError(response_post, 'form', 'text', _('This field is required.'))
        self.assertTemplateUsed(response_post, 'app_blog/create_blog.html')
        self.assertEqual(response_post.resolver_match.func.__name__, views.CreateBlogView.as_view().__name__)

    def test_post_create_blog_auth_user_with_fool_data(self):
        """
        Тестирование POST запроса аутентифицированного пользователя, при вводе в форму всех данных.
        """
        self.client.login(username=self.username, password=self.user_password)
        test_text = 'test text'
        current_datetime = datetime.datetime.now()
        current_datetime_str = current_datetime.strftime('%Y-%m-%dT%H:%M')

        with open(settings.BASE_DIR / 'project_modules/static/project_modules/images' / 'anonymous-photo.jpg',
                  mode='rb') as image:
            response_post = self.client.post(self.create_blog_url,
                                             {'text': test_text,
                                              'published_at': current_datetime_str,
                                              'images': image},
                                             follow=True)
        blog = models.Blog.objects.get(pk=1)
        uploaded_image_path = settings.BASE_DIR.joinpath(blog.images.all()[0].image.url.strip('/'))

        self.assertRedirects(response_post, reverse('app_blog:blog_detail', kwargs={'pk': 1}))
        self.assertEqual(blog.text, test_text)
        self.assertEqual(blog.published_at.strftime('%Y-%m-%dT%H:%M'), current_datetime_str)
        self.assertTrue(uploaded_image_path.exists())
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)
        uploaded_image_path.unlink()


class BlogDetailViewTest(TestCase):
    """
    Тестирование представления BlogDetailView
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    published_id = 1
    not_published_id = 2
    test_text = 'test text'
    published_date = timezone.now()

    @classmethod
    def setUpTestData(cls):
        user_inst = User(username=cls.username, email=cls.user_email)
        user_inst.set_password(cls.user_password)
        user_inst.save()
        models.Blog.objects.create(
            id=cls.published_id,
            text=cls.test_text,
            author=user_inst,
            published_at=cls.published_date
        )
        models.Blog.objects.create(
            id=cls.not_published_id,
            text=cls.test_text,
            author=user_inst,
        )

    def setUp(self):
        self.auth_url = reverse("app_users:login")
        self.published_detail_blog_url = reverse('app_blog:blog_detail',
                                                 kwargs={'pk': self.published_id})
        self.not_published_detail_blog_url = reverse('app_blog:blog_detail',
                                                     kwargs={'pk': self.not_published_id})

    def test_get_published_detail_blog(self):
        """
        Тестирование GET запроса к опубликованной записи
        """
        response_get = self.client.get(self.published_detail_blog_url)
        response_blog_context = response_get.context['blog']

        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_blog/blog_detail.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)

        self.assertEqual(response_blog_context.id, self.published_id)
        self.assertEqual(response_blog_context.text, self.test_text)
        self.assertEqual(response_blog_context.published_at, self.published_date)
        self.assertEqual(response_blog_context.author.id, 1)

    def test_get_not_published_detail_blog(self):
        """
        Тестирование GET запроса к неопубликованной записи.
        """
        response_get = self.client.get(self.not_published_detail_blog_url, follow=True)

        self.assertEqual(response_get.status_code, 403)
        self.assertEqual(response_get.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)

    def test_get_not_published_detail_blog_by_owner(self):
        """
        Тестирование GET запроса владельцем записи к неопубликованной записи.
        """
        self.client.login(username=self.username, password=self.user_password)
        response_get = self.client.get(self.not_published_detail_blog_url, follow=True)

        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)

    def test_post_add_comment_to_published_blog_with_wrong_data(self):
        """
        Тестирование POST запроса на добавление комментария с неверными данными
        """
        response_post = self.client.post(self.published_detail_blog_url, {'text': ''})
        self.assertEqual(response_post.status_code, 200)
        self.assertFormError(response_post, 'form', 'text', _('This field is required.'))
        self.assertTemplateUsed(response_post, 'app_blog/blog_detail.html')
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)

    def test_post_add_comment_to_published_blog_with_fool_data(self):
        """
        Тестирование POST запроса на добавление комментария с полными данными
        """
        test_text = 'test text'

        response_post = self.client.post(self.published_detail_blog_url, {'text': test_text}, follow=True)
        self.assertRedirects(response_post, self.published_detail_blog_url)
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)

        comment = models.BlogComment.objects.get(pk=1)
        self.assertEqual(comment.text, test_text)
        self.assertEqual(comment.user, None)
        self.assertEqual(comment.blog.id, self.published_id)
        self.assertTrue(comment.created_at)

    def test_post_add_comment_to_not_published_blog(self):
        """
        Тестирование POST запроса на добавление комментария к неопубликованному блогу
        """
        response_post = self.client.post(self.not_published_detail_blog_url, {'text': 'text'})

        self.assertEqual(response_post.status_code, 403)
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)


class BlogUpdateViewTest(TestCase):
    """
    Тестирование представления BlogUpdateView
    """
    blog_owner_username = 'blog_owner_username'
    blog_owner_email = 'test@test.ru'
    blog_owner_telephone_number = '1'

    another_user_username = 'another_user_name'
    another_user_email = 'another_user_name'
    another_user_telephone_number = '2'

    user_password = '123qweQWE'

    published_id = 1
    first_test_text = 'test text'
    published_date = timezone.now()

    @classmethod
    def setUpTestData(cls):
        blog_owner = User(username=cls.blog_owner_username,
                          email=cls.blog_owner_email,
                          telephone_number=cls.blog_owner_telephone_number)
        blog_owner.set_password(cls.user_password)
        blog_owner.save()

        another_user = User(username=cls.another_user_username,
                            email=cls.another_user_email,
                            telephone_number=cls.another_user_telephone_number)
        another_user.set_password(cls.user_password)
        another_user.save()

        models.Blog.objects.create(
            id=cls.published_id,
            text=cls.first_test_text,
            author=blog_owner,
            published_at=cls.published_date
        )

    def setUp(self):
        self.auth_url = reverse("app_users:login")
        self.update_blog_url = reverse('app_blog:blog_update',
                                       kwargs={'pk': self.published_id})

    def test_get_update_blog_not_auth_user(self):
        """
        Тестирование GET запроса неаутентифицированного пользователя
        """
        response_get = self.client.get(self.update_blog_url, follow=True)
        self.assertRedirects(response_get, f'{self.auth_url}?next={self.update_blog_url}')
        self.assertEqual(response_get.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_update_blog_with_another_user(self):
        """
        Тестирование GET запроса не владельцем блога
        """
        self.client.login(username=self.another_user_username, password=self.user_password)

        response_get = self.client.get(self.update_blog_url, follow=True)
        self.assertEqual(response_get.status_code, 403)
        self.assertEqual(response_get.resolver_match.func.__name__, views.BlogUpdateView.as_view().__name__)

    def test_get_update_blog_with_blog_owner(self):
        """
        Тестирование GET запроса владельцем блога
        """
        self.client.login(username=self.blog_owner_username, password=self.user_password)

        response_get = self.client.get(self.update_blog_url, follow=True)
        response_blog_context = response_get.context['blog']

        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_blog/update_blog.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.BlogUpdateView.as_view().__name__)

        self.assertEqual(response_blog_context.id, self.published_id)
        self.assertEqual(response_blog_context.text, self.first_test_text)
        self.assertEqual(response_blog_context.published_at, self.published_date)
        self.assertEqual(response_blog_context.author.id, 1)

    def test_post_update_blog_with_blog_owner_with_wrong_data(self):
        """
        Тестирование POST запроса владельцем блога с неверными данными
        """
        self.client.login(username=self.blog_owner_username, password=self.user_password)

        response_post = self.client.post(self.update_blog_url, {'text': ''}, follow=True)

        self.assertEqual(response_post.status_code, 200)
        self.assertTemplateUsed(response_post, 'app_blog/update_blog.html')
        self.assertFormError(response_post, 'form', 'text', _('This field is required.'))
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogUpdateView.as_view().__name__)

    def test_post_update_blog_with_blog_owner_with_fool_data(self):
        """
        Тестирование POST запроса владельцем блога с верными данными
        """

        second_test_text = 'new text'
        self.client.login(username=self.blog_owner_username, password=self.user_password)

        response_post = self.client.post(self.update_blog_url, {'text': second_test_text}, follow=True)

        blog = models.Blog.objects.get(pk=self.published_id)

        self.assertEqual(blog.text, second_test_text)
        self.assertNotEqual(blog.text, self.first_test_text)
        self.assertRedirects(response_post, reverse('app_blog:blog_detail',
                                                    kwargs={'pk': self.published_id}))
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogDetailView.as_view().__name__)


class BlogDeleteViewTest(TestCase):
    """
    Тестирование представления BlogDeleteView
    """
    blog_owner_username = 'blog_owner_username'
    blog_owner_email = 'test@test.ru'
    blog_owner_telephone_number = '1'

    user_password = '123qweQWE'

    blog_id = 1
    test_text = 'test text'
    published_date = timezone.now()

    @classmethod
    def setUpTestData(cls):
        blog_owner = User(username=cls.blog_owner_username,
                          email=cls.blog_owner_email,
                          telephone_number=cls.blog_owner_telephone_number)
        blog_owner.set_password(cls.user_password)
        blog_owner.save()

        models.Blog.objects.create(
            id=cls.blog_id,
            text=cls.test_text,
            author=blog_owner,
            published_at=cls.published_date
        )

    def setUp(self):
        self.delete_blog_url = reverse('app_blog:blog_delete',
                                       kwargs={'pk': self.blog_id})

    def test_get_delete_blog_not_auth_user(self):
        """
        Тестирование GET запроса неаутентифицированного пользователя
        """
        response_get = self.client.get(self.delete_blog_url, follow=True)
        self.assertEqual(response_get.status_code, 403)
        self.assertEqual(response_get.resolver_match.func.__name__, views.BlogDeleteView.as_view().__name__)

    def test_post_delete_blog_not_auth_user(self):
        """
        Тестирование POST запроса неаутентифицированного пользователя
        """
        response_post = self.client.post(self.delete_blog_url, follow=True)
        self.assertEqual(response_post.status_code, 403)
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogDeleteView.as_view().__name__)

    def test_get_delete_blog_with_blog_owner(self):
        """
        Тестирование GET запроса владельцем блога
        """
        self.client.login(username=self.blog_owner_username, password=self.user_password)

        response_get = self.client.get(self.delete_blog_url, follow=True)
        self.assertRedirects(response_get, reverse('app_users:user_list'))
        self.assertEqual(response_get.resolver_match.func.__name__, CustomUserListView.as_view().__name__)

    def test_post_delete_blog_with_blog_owner(self):
        """
        Тестирование POST запроса владельцем блога
        """
        self.client.login(username=self.blog_owner_username, password=self.user_password)

        blog = models.Blog.objects.get(id=self.blog_id)
        self.assertTrue(blog)

        response_post = self.client.post(self.delete_blog_url, follow=True)
        self.assertRedirects(response_post, reverse('app_users:user_list'))
        self.assertEqual(response_post.resolver_match.func.__name__, CustomUserListView.as_view().__name__)

        with self.assertRaises(models.Blog.DoesNotExist):
            models.Blog.objects.get(id=self.blog_id)


class DeleteBlogImageViewTest(TestCase):
    """
    Тестирование представления DeleteBlogImage
    """
    blog_owner_username = 'blog_owner_username'
    blog_owner_email = 'test@test.ru'
    blog_owner_telephone_number = '1'

    user_password = '123qweQWE'

    blog_id = blog_image_id = 1
    test_text = 'test text'
    published_date = timezone.now()

    @classmethod
    def setUpTestData(cls):
        blog_owner = User(username=cls.blog_owner_username,
                          email=cls.blog_owner_email,
                          telephone_number=cls.blog_owner_telephone_number)
        blog_owner.set_password(cls.user_password)
        blog_owner.save()

        blog = models.Blog.objects.create(
            id=cls.blog_id,
            text=cls.test_text,
            author=blog_owner,
            published_at=cls.published_date
        )
        with open(settings.BASE_DIR / 'project_modules/static/project_modules/images' / 'anonymous-photo.jpg',
                  mode='rb') as image:
            db_image = InMemoryUploadedFile(image,
                                            'ImageField',
                                            'test_img.jpg',
                                            'jpeg/image',
                                            sys.getsizeof(image),
                                            None)
            models.BlogImage.objects.create(id=cls.blog_image_id, image=db_image, blog=blog)

    def setUp(self):
        self.delete_blog_image_url = reverse('app_blog:blog_image_delete',
                                             kwargs={'pk': self.blog_image_id})

    def test_get_delete_blog_not_auth_user(self):
        """
        Тестирование GET запроса неаутентифицированного пользователя
        """
        response_get = self.client.get(self.delete_blog_image_url, follow=True)
        self.assertEqual(response_get.status_code, 403)
        self.assertEqual(response_get.resolver_match.func.__name__, views.DeleteBlogImageView.as_view().__name__)

    def test_post_delete_blog_not_auth_user(self):
        """
        Тестирование POST запроса неаутентифицированного пользователя
        """
        response_post = self.client.post(self.delete_blog_image_url, follow=True)
        self.assertEqual(response_post.status_code, 403)
        self.assertEqual(response_post.resolver_match.func.__name__, views.DeleteBlogImageView.as_view().__name__)

    def test_get_delete_blog_with_blog_owner(self):
        """
        Тестирование GET запроса владельцем блога
        """
        self.client.login(username=self.blog_owner_username, password=self.user_password)

        response_get = self.client.get(self.delete_blog_image_url, follow=True)
        self.assertRedirects(response_get, reverse('app_users:user_list'))
        self.assertEqual(response_get.resolver_match.func.__name__, CustomUserListView.as_view().__name__)

    def test_post_delete_blog_with_blog_owner(self):
        """
        Тестирование POST запроса владельцем блога
        """
        self.client.login(username=self.blog_owner_username, password=self.user_password)

        blog_image = models.BlogImage.objects.get(id=self.blog_image_id)
        uploaded_image_path = settings.BASE_DIR.joinpath(blog_image.image.url.strip('/'))
        self.assertTrue(blog_image)

        response_post = self.client.post(self.delete_blog_image_url, follow=True)
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogUpdateView.as_view().__name__)

        with self.assertRaises(models.BlogImage.DoesNotExist):
            models.BlogImage.objects.get(id=self.blog_image_id)

        uploaded_image_path.unlink()


class UserBlogListViewTest(TestCase):
    """
    Тестирование представления UserBlogListView
    """
    blog_owner_username = 'blog_owner_username'
    blog_owner_email = 'test@test.ru'
    blog_owner_telephone_number = '1'
    user_password = '123qweQWE'

    blogs_count = 100

    @classmethod
    def setUpTestData(cls):
        cls.blog_owner = User(username=cls.blog_owner_username,
                              email=cls.blog_owner_email,
                              telephone_number=cls.blog_owner_telephone_number)
        cls.blog_owner.set_password(cls.user_password)
        cls.blog_owner.save()

        cls.blog_list = []
        published_at = timezone.now()
        for i in range(1, cls.blogs_count + 1):
            blog = models.Blog(id=i, text=f'text {i}', author=cls.blog_owner,
                               published_at=published_at + datetime.timedelta(seconds=1))
            cls.blog_list.append(blog)
        models.Blog.objects.bulk_create(cls.blog_list)

    def setUp(self):
        self.blog_list_url = reverse('app_blog:user_blog_entries', kwargs={'pk': self.blog_owner.id,
                                                                           'slug': self.blog_owner.slug})

    def test_get_blog_list(self):
        """
        Тестирование GET запроса
        """
        response_get = self.client.get(self.blog_list_url)

        blog_entries = response_get.context['blog_entries']
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(blog_entries[0].id, 1)
        self.assertEqual(len(blog_entries), 12)
        self.assertTemplateUsed(response_get, 'app_blog/user_blog_list.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.UserBlogListView.as_view().__name__)

    def test_get_blog_list_page_2(self):
        """
        Тестирование GET запроса ко второй странице
        """
        response_get = self.client.get(f"{self.blog_list_url}?page=2")

        blog_entries = response_get.context['blog_entries']
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(len(blog_entries), 12)
        self.assertEqual(blog_entries[0].id, 13)
        self.assertTemplateUsed(response_get, 'app_blog/user_blog_list.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.UserBlogListView.as_view().__name__)

    def test_get_blog_list_with_custom_paginate(self):
        """
        Тестирование GET запроса с установкой пользовательской пагинатора
        """
        blog_entries_per_page = 24

        self.client.cookies['blog_entries_per_page'] = blog_entries_per_page
        response_get = self.client.get(self.blog_list_url)

        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(len(response_get.context['blog_entries']), blog_entries_per_page)
        self.assertTemplateUsed(response_get, 'app_blog/user_blog_list.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.UserBlogListView.as_view().__name__)


class BlogCreateFromFileViewTest(TestCase):
    """
    Тестирование представления BlogCreateFromFile
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        cls.user_inst = User(username=cls.username, email=cls.user_email)
        cls.user_inst.set_password(cls.user_password)
        cls.user_inst.save()

    def setUp(self):
        self.blog_create_from_file = reverse('app_blog:blog_create_from_file')
        self.auth_url = reverse("app_users:login")

    def test_get_create_blog_from_file_not_auth_user(self):
        """
        Тестирование GET запроса неаутентифицированного пользователя
        """
        response_get = self.client.get(self.blog_create_from_file, follow=True)
        self.assertRedirects(response_get, f'{self.auth_url}?next={self.blog_create_from_file}')
        self.assertEqual(response_get.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_get_create_blog_auth_user(self):
        """
        Тестирование GET запроса аутентифицированного пользователя
        """
        self.client.login(username=self.username, password=self.user_password)

        response_get = self.client.get(self.blog_create_from_file)
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'app_blog/create_blog_from_file.html')
        self.assertEqual(response_get.resolver_match.func.__name__, views.BlogCreateFromFileView.as_view().__name__)

    def test_post_create_blog_not_auth_user(self):
        """
        Тестирование POST запроса неаутентифицированного пользователя
        """
        response_post = self.client.post(self.blog_create_from_file, follow=True)
        self.assertRedirects(response_post, f'{self.auth_url}?next={self.blog_create_from_file}')
        self.assertEqual(response_post.resolver_match.func.__name__, LoginUserView.as_view().__name__)

    def test_post_create_blog_auth_user_with_wrong_data(self):
        """
        Тестирование POST запроса аутентифицированного пользователя, при вводе в форму неверных данных
        """
        self.client.login(username=self.username, password=self.user_password)

        with open(settings.BASE_DIR / 'app_blog/tests' / 'wrong_csv_test.csv',
                  mode='rb') as csv_file:
            response_post = self.client.post(self.blog_create_from_file, {'csv_file': csv_file})

        self.assertEqual(response_post.status_code, 200)
        self.assertFormError(response_post, 'form', 'csv_file', _('Invalid date format in the file'))
        self.assertTemplateUsed(response_post, 'app_blog/create_blog_from_file.html')
        self.assertEqual(response_post.resolver_match.func.__name__, views.BlogCreateFromFileView.as_view().__name__)

    def test_post_create_blog_auth_user_with_good_data(self):
        """
        Тестирование POST запроса аутентифицированного пользователя, при вводе в форму корректных данных
        """
        self.client.login(username=self.username, password=self.user_password)

        with open(settings.BASE_DIR / 'app_blog/tests' / 'csv_test.csv',
                  mode='rb') as csv_file:
            response_post = self.client.post(self.blog_create_from_file, {'csv_file': csv_file}, follow=True)

        redirect_url = reverse('app_blog:user_blog_entries',
                               kwargs={'pk': self.user_inst.pk, 'slug': self.user_inst.slug, })
        self.assertRedirects(response_post, f'{redirect_url}?page=last')
        self.assertEqual(response_post.resolver_match.func.__name__, views.UserBlogListView.as_view().__name__)
