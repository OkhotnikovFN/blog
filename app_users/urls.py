from django.urls import path

from app_users import views


app_name = 'app_users'

urlpatterns = [
    path('bloger_list/', views.CustomUserListView.as_view(), name='user_list'),
    path('<slug:slug>_<int:pk>/', views.CustomUserUpdateView.as_view(), name='personal_account'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutCustomUserView.as_view(), name='logout'),
    path('change_password/', views.CustomUserChangePasswordView.as_view(), name='change_password'),
    path('register/', views.RegisterCustomUserView.as_view(), name='register'),
    path('delete/<slug:slug>_<int:pk>', views.DeleteCustomUserView.as_view(), name='delete'),
]
