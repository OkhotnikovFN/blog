from django.db import models
from django.urls import reverse

from app_users.models import CustomUser


class Blog(models.Model):
    """Модель блога"""
    text = models.TextField('Текст блога')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='blog', )
    published_at = models.DateTimeField('Дата публикации', null=True, blank=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
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
    image = models.ImageField('Фото блога', upload_to='blogs/images/',)
    blog = models.ForeignKey(Blog,
                             on_delete=models.CASCADE,
                             verbose_name='Изображение блога',
                             related_name='images', )

    class Meta:
        verbose_name = 'Изображение блога'
        verbose_name_plural = 'Изображения блога'

    def __str__(self):
        return f'{self.image.name}'


class BlogComment(models.Model):
    """
    Модель комментариев к записи блога
    """
    user = models.ForeignKey(CustomUser,
                             on_delete=models.SET_NULL,
                             verbose_name='Пользователь',
                             related_name='comments',
                             blank=True,
                             null=True, )

    text = models.TextField('Комментарий')
    blog = models.ForeignKey(Blog,
                             on_delete=models.CASCADE,
                             verbose_name='Запись блога',
                             related_name='comments', )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

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



