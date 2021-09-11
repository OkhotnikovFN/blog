from django.contrib.auth import get_user_model


class CustomAuthBackend:
    """
    Базовый класс для аутентификации пользователей
    """
    auth_field = None

    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        filter_kwargs = {self.auth_field: username}
        try:
            user = User.objects.get(**filter_kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except Exception:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
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
