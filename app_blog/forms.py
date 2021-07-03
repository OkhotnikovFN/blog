import csv
import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from app_blog import models, widgets
from project_modules.forms import ChangeIsValidFormMixin

FIELDS_HELP_TEXT_AND_ATTRIBUTES = {
    'text': {
        'help_text': 'Введите текст блога',
        'attributes': {'placeholder': 'Текст блога',
                       'aria-label': 'Введите текст блога', },
    },
    'published_at': {
        'help_text': 'Введите дату публикации',
        'attributes': {'placeholder': 'Дата публикации',
                       'aria-label': 'Дата публикации', },
    },
    'images': {
        'help_text': 'Выберите изображения',
        'attributes': {'placeholder': 'Выберите изображения',
                       'aria-label': 'Выберите изображения',
                       'multiple': True, },
    },
}

FORM_CLASS_NAME = 'create-blog-form__field'


class BlogForm(forms.ModelForm, ChangeIsValidFormMixin):
    """Форма создания блога"""

    images = forms.ImageField(label='Изображения', required=False)

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)

        for field_name in ['text', 'published_at', 'images']:
            self.fields[field_name].help_text = FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['help_text']

        for field in self.fields.values():
            field.widget.attrs.update({'class': FORM_CLASS_NAME,
                                       'title': f'{field.help_text}', })

        for field_name in ['text', 'published_at', 'images']:
            self.fields[field_name].widget.attrs.update(FIELDS_HELP_TEXT_AND_ATTRIBUTES[field_name]['attributes'])

    class Meta:
        model = models.Blog
        exclude = ['author']
        widgets = {
            'published_at': widgets.CustomDateTimeInput(format='%Y-%m-%dT%H:%M'),
        }


class BlogCommentForm(forms.ModelForm, ChangeIsValidFormMixin):
    """
    Форма для создания комментария к записи блога.
    """

    class Meta:
        model = models.BlogComment
        exclude = ['user', 'blog']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'create-blog-form__field',
                'placeholder': 'Введите комментарий',
                'aria-label': 'Введите комментарий',
            }),
        }


class BlogEntriesFileForm(forms.Form, ChangeIsValidFormMixin):
    """Форма для создания записей блога, из CSV файла"""
    csv_file = forms.FileField(label='CSV файл', validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    csv_file.widget.attrs.update({'class': FORM_CLASS_NAME})

    def clean_csv_file(self):
        """Проверка файла на правильность кодировки и правильность структуры файла
         и передача в представление списка данных из файла"""
        from app_blog import services
        data_list = services.check_csv_blog_file(self.cleaned_data['csv_file'])

        return data_list
