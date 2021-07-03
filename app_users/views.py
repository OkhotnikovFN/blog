from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, UpdateView, DeleteView

from project_modules.views import CustomPaginateListView
from app_users import forms, models, services


class LoginUserView(LoginView):
    """
    Вход на сайт под своим пользователем.
    """
    form_class = forms.AuthForm
    template_name = 'app_users/login.html'
    redirect_authenticated_user = True


class LogoutCustomUserView(LogoutView):
    """
    Выход с сайта.
    """
    next_page = reverse_lazy('main_view')


class RegisterCustomUserView(FormView):
    """
    Регистрация нового пользователя.
    """
    form_class = forms.CustomUserCreationForm
    template_name = 'app_users/register.html'
    success_url = reverse_lazy('main_view')

    def form_valid(self, form):
        services.create_new_user(form)
        user = services.authenticate_user(form)
        login(self.request, user)
        return super(RegisterCustomUserView, self).form_valid(form)


class CustomUserIsOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Проверка является ли пользователь владельцем своей личной страницы"""
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        return redirect(reverse('app_users:user_list'))


class DeleteCustomUserView(CustomUserIsOwnerMixin, DeleteView):
    """Удаление пользователем своей страницы"""
    model = models.CustomUser
    query_pk_and_slug = True
    success_url = reverse_lazy('main_view')

    def get(self, request, *args, **kwargs):
        return redirect(reverse('main_view'))


class CustomUserListView(CustomPaginateListView):
    """
    Представление для вывода списка пользователей.
    """
    queryset = models.CustomUser.objects.all().order_by('username')
    context_object_name = 'users'
    paginate_cookie_name = 'users_per_page'
    template_name = 'app_users/user_list.html'

    def get_queryset(self):
        queryset = super(CustomUserListView, self).get_queryset()
        queryset = services.filter_users_queryset_by_username(queryset, self.request)

        return queryset


class CustomUserUpdateView(CustomUserIsOwnerMixin, UpdateView):
    """Обновление инвормации о своей странице"""
    template_name = 'app_users/personal_account.html'
    form_class = forms.CustomUserChangeForm
    model = models.CustomUser
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super(CustomUserUpdateView, self).get_context_data(**kwargs)
        context['pass_successfully_changed'] = self.request.GET.get('pass_successfully_changed')

        return context


class CustomUserChangePasswordView(PasswordChangeView):
    """
    Изменение пароля пользователя.
    """
    form_class = forms.UserChangePasswordForm
    template_name = 'app_users/custom_user_password_change.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            pk = self.request.user.pk
            slug = self.request.user.slug
            url = reverse('app_users:personal_account', kwargs={'pk': pk, 'slug': slug})
            return f'{url}?pass_successfully_changed=True'

        return reverse('main_view')
