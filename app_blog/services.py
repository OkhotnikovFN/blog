import csv
import datetime
from typing import List

from django.core.exceptions import ValidationError
from django.forms import FileField
from django.http import HttpRequest
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from app_blog import models, forms
from app_blog.forms import BlogCommentForm, BlogEntriesFileForm
from app_blog.models import Blog


def create_update_blog(form: forms.BlogForm, request: HttpRequest) -> models.Blog:
    """
    Создание записи блога.
    """
    blog = form.save(commit=False)
    blog.author = request.user
    blog.save()
    images = request.FILES.getlist('images')

    for image in images:
        blog_image = models.BlogImage(image=image, blog=blog)
        blog_image.save()

    return blog


def create_blog_comment(form: BlogCommentForm, request: HttpRequest, blog: Blog):
    """
    Создание нового комментария к записи блога.
    """
    new_comment = form.save(commit=False)
    new_comment.blog = blog
    active_user = request.user

    if active_user.is_authenticated:
        new_comment.user = active_user

    new_comment.save()


def create_blog_from_file(form: BlogEntriesFileForm, request: HttpRequest):
    """Создание записей блога из CSV файла"""
    blog_list = []
    for data_row in form.cleaned_data['csv_file']:
        blog_list.append(models.Blog(text=data_row[0],
                                     published_at=data_row[1],
                                     author=request.user))

    models.Blog.objects.bulk_create(blog_list)


def check_csv_blog_file(form_data: FileField.clean) -> List:
    """Проверка файла на правильность кодировки и правильность структуры файла"""
    csv_file = form_data
    csv_file_bytes = csv_file.read()

    try:
        csv_file_str = csv_file_bytes.decode('utf8').split('\n')
    except UnicodeDecodeError:
        raise ValidationError(_('Invalid file encoding'))

    csv_reader = csv.reader(csv_file_str, delimiter=':', quotechar='"')
    data_list = list(csv_reader)

    for csv_row in data_list:
        try:
            csv_row[1] = localtime(datetime.datetime.strptime(csv_row[1], '%Y-%m-%dT%H:%M%z'))
        except ValueError:
            raise ValidationError(_('Invalid date format in the file'))

    return data_list
