from django import forms
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

from app_blog import models, widgets
from project_modules.forms import ChangeIsValidFormMixin

FIELDS_HELP_TEXT_AND_ATTRIBUTES = {
    'text': {
        'help_text': _('Enter blog text'),
        'attributes': {'placeholder': _('Blog text'),
                       'aria-label': _('Enter blog text'), },
    },
    'published_at': {
        'help_text': _('Enter published date'),
        'attributes': {'placeholder': _('Published date'),
                       'aria-label': _('Published date'), },
    },
    'images': {
        'help_text': _('Select Images'),
        'attributes': {'placeholder': _('Select Images'),
                       'aria-label': _('Select Images'),
                       'multiple': True, },
    },
}

FORM_CLASS_NAME = 'create-blog-form__field'


class BlogForm(forms.ModelForm, ChangeIsValidFormMixin):
    """Форма создания блога"""

    images = forms.ImageField(label=_('Images'), required=False)

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
                'class': FORM_CLASS_NAME,
                'placeholder': _('Enter a comment'),
                'aria-label': _('Enter a comment'),
            }),
        }


class BlogEntriesFileForm(forms.Form, ChangeIsValidFormMixin):
    """Форма для создания записей блога, из CSV файла"""
    csv_file = forms.FileField(label=_('CSV file'), validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    csv_file.widget.attrs.update({'class': FORM_CLASS_NAME})

    def clean_csv_file(self):
        """Проверка файла на правильность кодировки и правильность структуры файла
         и передача в представление списка данных из файла"""
        from app_blog import services
        data_list = services.check_csv_blog_file(self.cleaned_data['csv_file'])

        return data_list
