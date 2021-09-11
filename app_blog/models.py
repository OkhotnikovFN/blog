from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app_users.models import CustomUser


class Blog(models.Model):
    """Модель блога"""
    text = models.TextField(_('Blog text'))
    created_at = models.DateTimeField(_('Created date'), auto_now_add=True)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               verbose_name=_('Author'),
                               related_name='blog', )
    published_at = models.DateTimeField(_('Published date'), null=True, blank=True)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('app_blog:blog_detail', kwargs={'pk': str(self.id)})

    @property
    def display_text(self):
        """
        Частично отобразить текст блога.
        """
        len_to_display = 100
        text = self.text
        return f'{text[:len_to_display]}...' if len(text) > len_to_display else text

    def __str__(self):
        return self.display_text


class BlogImage(models.Model):
    """Модель изображения для блога"""
    image = models.ImageField(_('Blog image'), upload_to='blogs/images/',)
    blog = models.ForeignKey(Blog,
                             on_delete=models.CASCADE,
                             verbose_name=_('Blog Entry'),
                             related_name='images', )

    class Meta:
        verbose_name = _('Blog image')
        verbose_name_plural = _('Blog images')

    def __str__(self):
        return f'{self.image.name}'


class BlogComment(models.Model):
    """
    Модель комментариев к записи блога
    """
    user = models.ForeignKey(CustomUser,
                             on_delete=models.SET_NULL,
                             verbose_name=_('User'),
                             related_name='comments',
                             blank=True,
                             null=True, )

    text = models.TextField(_('Comment'))
    blog = models.ForeignKey(Blog,
                             on_delete=models.CASCADE,
                             verbose_name=_('Blog Entry'),
                             related_name='comments', )
    created_at = models.DateTimeField(_('Created date'), auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    @property
    def display_text(self):
        """
        Частично отобразить текст комментария.
        """
        len_to_display = 100
        text = self.text
        return f'{text[:len_to_display]}...' if len(text) > len_to_display else text

    def __str__(self):
        return self.display_text



