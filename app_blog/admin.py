from django.contrib import admin

from app_blog.models import Blog, BlogImage, BlogComment


@admin.register(Blog)
class AdminCustomUser(admin.ModelAdmin):
    """Административная панель для модели Blog"""
    pass


@admin.register(BlogImage)
class AdminCustomUser(admin.ModelAdmin):
    """Административная панель для модели BlogImages"""
    pass


@admin.register(BlogComment)
class AdminBlogComment(admin.ModelAdmin):
    """Административная панель для модели BlogComment"""
    pass
