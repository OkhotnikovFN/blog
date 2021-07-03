from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from project_modules.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main_view'),
    path('bloger/', include('app_users.urls')),
    path('blog/', include('app_blog.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
