from django.contrib.auth import authenticate
from django.db.models import QuerySet
from django.http import HttpRequest

from app_users import forms, models


def filter_users_queryset_by_username(queryset: QuerySet, request: HttpRequest) -> QuerySet:
    """
    Регистронезависимя фильтрация запорса пользователей по полю username.
    """
    username = request.GET.get('username')

    if username:
        queryset = queryset.filter(username__icontains=username)

    return queryset


def create_new_user(form: forms.CustomUserCreationForm):
    """
    Создание нового пользователя.
    """
    form.save()


def authenticate_user(form: forms.CustomUserCreationForm) -> models.CustomUser:
    """
    Аутентификация пользователя.
    """
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)

    return user
