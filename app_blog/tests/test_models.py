import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from app_blog import models

User = get_user_model()


class BlogModelTest(TestCase):
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
        models.Blog.objects.create(id=1,
                                   text='test text',
                                   author=user_inst,
                                   published_at=timezone.now())
        models.Blog.objects.create(id=2,
                                   text='test text' * 100,
                                   author=user_inst,
                                   published_at=timezone.now())

    def test_text_label(self):
        """
        Тестирование verbose_name у поля text
        """
        blog = models.Blog.objects.get(id=1)
        field_label = blog._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Текст блога')

    def test_created_at_label(self):
        """
        Тестирование verbose_name у поля created_at
        """
        blog = models.Blog.objects.get(id=1)
        field_label = blog._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Дата создания')

    def test_author_label(self):
        """
        Тестирование verbose_name у поля author
        """
        blog = models.Blog.objects.get(id=1)
        field_label = blog._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_published_at_label(self):
        """
        Тестирование verbose_name у поля published_at
        """
        blog = models.Blog.objects.get(id=1)
        field_label = blog._meta.get_field('published_at').verbose_name
        self.assertEquals(field_label, 'Дата публикации')

    def test_get_absolute_url(self):
        """
        Тестирование метода get_absolute_url
        """
        blog = models.Blog.objects.get(id=1)
        self.assertEquals(blog.get_absolute_url(), reverse('app_blog:blog_detail', kwargs={'pk': 1}))

    def test_short_str_represent_name(self):
        """
        Тестирование текстового представления блога при коротком значении поля text
        """
        blog = models.Blog.objects.get(id=1)
        expected_object_name = f'{blog.text}'
        self.assertEquals(expected_object_name, str(blog))

    def test_long_str_represent_name(self):
        """
        Тестирование текстового представления блога при длинном значении поля text
        """
        len_to_display = 100
        blog = models.Blog.objects.get(id=2)
        expected_object_name = f'{blog.text[:len_to_display]}...'
        self.assertEquals(expected_object_name, str(blog))


class BlogImageModelTest(TestCase):
    """
    Тестирование модели BlogImage
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        user_inst = User(username=cls.username, email=cls.user_email)
        user_inst.set_password(cls.user_password)
        user_inst.save()
        blog = models.Blog.objects.create(id=1,
                                          text='test text',
                                          author=user_inst,
                                          published_at=timezone.now())
        with open(settings.BASE_DIR / 'project_modules/static/project_modules/images' / 'anonymous-photo.jpg',
                  mode='rb') as image:
            db_image = InMemoryUploadedFile(image,
                                            'ImageField',
                                            'test_img.jpg',
                                            'jpeg/image',
                                            sys.getsizeof(image),
                                            None)
            models.BlogImage.objects.create(id=1, image=db_image, blog=blog)

    def test_image_label(self):
        """
        Тестирование verbose_name у поля image
        """
        blog_image = models.BlogImage.objects.get(id=1)
        field_label = blog_image._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'Фото блога')

    def test_created_at_label(self):
        """
        Тестирование verbose_name у поля blog
        """
        blog_image = models.BlogImage.objects.get(id=1)
        field_label = blog_image._meta.get_field('blog').verbose_name
        self.assertEquals(field_label, 'Изображение блога')

    def test_str_represent_name(self):
        """
        Тестирование текстового представления модели BlogImage
        """
        blog_image = models.BlogImage.objects.get(id=1)
        expected_object_name = f'{blog_image.image.name}'
        self.assertEquals(expected_object_name, str(blog_image))

        uploaded_image_path = settings.BASE_DIR.joinpath(blog_image.image.url.strip('/'))
        uploaded_image_path.unlink()


class BlogCommentModelTest(TestCase):
    """
    Тестирование модели BlogComment
    """
    username = 'test_username'
    user_email = 'test@test.ru'
    user_password = '123qweQWE'

    @classmethod
    def setUpTestData(cls):
        user_inst = User(username=cls.username, email=cls.user_email)
        user_inst.set_password(cls.user_password)
        user_inst.save()
        blog = models.Blog.objects.create(id=1,
                                          text='test text',
                                          author=user_inst,
                                          published_at=timezone.now())
        models.BlogComment.objects.create(id=1,
                                          user=user_inst,
                                          text='test_text',
                                          blog=blog)
        models.BlogComment.objects.create(id=2,
                                          user=user_inst,
                                          text='test_text' * 100,
                                          blog=blog)

    def test_user_label(self):
        """
        Тестирование verbose_name у поля user
        """
        blog_comment = models.BlogComment.objects.get(id=1)
        field_label = blog_comment._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_text_label(self):
        """
        Тестирование verbose_name у поля text
        """
        blog_comment = models.BlogComment.objects.get(id=1)
        field_label = blog_comment._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Комментарий')

    def test_blog_label(self):
        """
        Тестирование verbose_name у поля blog
        """
        blog_comment = models.BlogComment.objects.get(id=1)
        field_label = blog_comment._meta.get_field('blog').verbose_name
        self.assertEquals(field_label, 'Запись блога')

    def test_short_str_represent_name(self):
        """
        Тестирование текстового представления комментария при коротком значении поля text
        """
        blog_comment = models.BlogComment.objects.get(id=1)
        expected_object_name = f'{blog_comment.text}'
        self.assertEquals(expected_object_name, str(blog_comment))

    def test_long_str_represent_name(self):
        """
        Тестирование текстового представления комментария при длинном значении поля text
        """
        len_to_display = 100
        blog_comment = models.BlogComment.objects.get(id=2)
        expected_object_name = f'{blog_comment.text[:len_to_display]}...'
        self.assertEquals(expected_object_name, str(blog_comment))
