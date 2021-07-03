from django.contrib.auth import get_user_model


class CustomAuthBackend:
    """
    Базовый класс для аутентификации пользователей
    """
    auth_field = None

    def authenticate(self, request, username=None, password=None):
        my_user_model = get_user_model()
        filter_kwargs = {self.auth_field: username}
        try:
            user = my_user_model.objects.get(**filter_kwargs)
            if user.check_password(password):
                return user
        except my_user_model.DoesNotExist:
            return None
        except Exception:
            return None

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None


class EmailBackend(CustomAuthBackend):
    """
    Добавление аутентификации по email пользователя
    """
    auth_field = 'email'


class TelephoneBackend(CustomAuthBackend):
    """
    Добавление аутентификации по email пользователя
    """
    auth_field = 'telephone_number'
