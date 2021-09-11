from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Расширенная модель пользователя
    """
    email = models.EmailField(_('email address'), unique=True)
    telephone_number = models.CharField(_('telephone number'),
                                        max_length=20,
                                        unique=True, )
    user_photo = models.ImageField(_('profile photo'), upload_to='users/photos/', blank=True, null=True)
    slug = models.SlugField('slug-url')

    def get_absolute_url(self):
        return reverse('app_users:personal_account', kwargs={'pk': str(self.id), 'slug': self.slug})
