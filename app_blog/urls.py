from django.urls import path

from app_blog import views


app_name = 'app_blog'

urlpatterns = [
    path('blog_create/', views.CreateBlogView.as_view(), name='blog_create'),
    path('blog_create_from_file/', views.BlogCreateFromFileView.as_view(), name='blog_create_from_file'),
    path('blog_detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog_update/<int:pk>/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog_image_delete/<int:pk>/', views.DeleteBlogImageView.as_view(), name='blog_image_delete'),
    path('user_blog_entries/<slug:slug>_<int:pk>/', views.UserBlogListView.as_view(), name='user_blog_entries'),
]
