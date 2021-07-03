from django.db.models import signals
from django.dispatch import receiver
from uuslug import slugify

from app_users.models import CustomUser


@receiver(signals.pre_save, sender=CustomUser)
def make_slug(sender, instance: CustomUser, *args, **kwargs):
    """
    Сигнал добавления поля slug к экземпляру модели CustomUser.
    """
    instance.slug = slugify(instance.username)
