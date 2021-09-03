import sys

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from app_blog import forms
from app_blog.widgets import CustomDateTimeInput

User = get_user_model()


class BlogFormTest(TestCase):
    """
    Тестирование формы BlogForm
    """

    def setUp(self):
        self.form = forms.BlogForm()

    def test_images_field_help_text(self):
        """
        Тестирование help_text у поля images
        """
        self.assertEqual(self.form.fields['images'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['images']['help_text'])

    def test_text_field_help_text(self):
        """
        Тестирование help_text у поля text
        """
        self.assertEqual(self.form.fields['text'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['text']['help_text'])

    def test_published_at_field_help_text(self):
        """
        Тестирование help_text у поля published_at
        """
        self.assertEqual(self.form.fields['published_at'].help_text,
                         forms.FIELDS_HELP_TEXT_AND_ATTRIBUTES['published_at']['help_text'])

    def test_published_at_field_widget(self):
        """
        Тестирование widget у поля published_at
        """
        self.assertTrue(isinstance(self.form.fields['published_at'].widget, CustomDateTimeInput))

    def test_fields_count(self):
        """
        Тестирование колличества и качества полей в форме
        """
        self.assertEqual(len(self.form.fields), 3)

        for field_name in ['text', 'published_at', 'images']:
            self.assertTrue(field_name in self.form.fields)


class BlogCommentFormTest(TestCase):
    """
    Тестирование формы BlogCommentForm
    """

    def test_fields_count(self):
        """
        Тестирование количества и качества полей в форме
        """
        form = forms.BlogCommentForm()
        self.assertEqual(len(form.fields), 1)

        self.assertTrue('text' in form.fields)


class BlogEntriesFileFormTest(TestCase):
    """
    Тестирование формы BlogEntriesFileForm
    """

    def test_images_field_label(self):
        """
        Тестирование label у поля csv_file
        """
        form = forms.BlogEntriesFileForm()
        self.assertEqual(form.fields['csv_file'].label, 'CSV файл')

    def test_valid_file_extension(self):
        """
        Тестирование валидности расширения входящего файла
        """
        with open(settings.BASE_DIR / 'project_modules/static/project_modules/images' / 'anonymous-photo.jpg',
                  mode='rb') as image:
            form_img = InMemoryUploadedFile(image,
                                            'FileField',
                                            'anonymous-photo.jpg',
                                            'file',
                                            sys.getsizeof(image),
                                            None)
            form = forms.BlogEntriesFileForm(files={'csv_file': form_img})

            self.assertFalse(form.is_valid())

        with open(settings.BASE_DIR / 'app_blog/tests' / 'csv_test.csv',
                  mode='rb') as csv_file:
            form_csv = InMemoryUploadedFile(csv_file,
                                            'FileField',
                                            'csv_test.csv',
                                            'file',
                                            sys.getsizeof(csv_file),
                                            None)
            form = forms.BlogEntriesFileForm(files={'csv_file': form_csv})

            self.assertTrue(form.is_valid())

    def test_valid_file_structure(self):
        """
        Тестирование валидности структуры входящего csv файла, при правильной структуре
        """
        with open(settings.BASE_DIR / 'app_blog/tests' / 'csv_test.csv',
                  mode='rb') as csv_file:
            form_csv = InMemoryUploadedFile(csv_file,
                                            'FileField',
                                            'csv_test.csv',
                                            'file',
                                            sys.getsizeof(csv_file),
                                            None)
            form = forms.BlogEntriesFileForm(files={'csv_file': form_csv})

            self.assertTrue(form.is_valid())

    def test_not_valid_file_structure(self):
        """
        Тестирование валидности структуры входящего csv файла, при неправильной структуре
        """
        with open(settings.BASE_DIR / 'app_blog/tests' / 'wrong_csv_test.csv',
                  mode='rb') as csv_file:
            form_csv = InMemoryUploadedFile(csv_file,
                                            'FileField',
                                            'csv_test.csv',
                                            'file',
                                            sys.getsizeof(csv_file),
                                            None)
            form = forms.BlogEntriesFileForm(files={'csv_file': form_csv})

            self.assertFalse(form.is_valid())
