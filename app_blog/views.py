from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from app_blog import models, forms, services
from project_modules.views import CustomPaginateListView


class CreateBlogView(LoginRequiredMixin, generic.CreateView):
    """Представление создания записи блога"""
    template_name = 'app_blog/create_blog.html'
    form_class = forms.BlogForm
    login_url = reverse_lazy('app_users:login')

    def form_valid(self, form):
        self.object = services.create_update_blog(form, self.request)

        return super(generic.CreateView, self).form_valid(form)


class BlogDetailView(UserPassesTestMixin, generic.DetailView, generic.FormView):
    """Представление детальрного просмотра записи блога"""
    template_name = 'app_blog/blog_detail.html'
    queryset = models.Blog.objects.select_related('author').prefetch_related(
        Prefetch('images', queryset=models.BlogImage.objects.all(), to_attr='all_images'),
        Prefetch('comments',
                 queryset=models.BlogComment.objects.select_related('user').order_by('-created_at'),
                 to_attr='all_comments'),
    )
    form_class = forms.BlogCommentForm
    raise_exception = True

    def test_func(self):
        blog = self.get_object()
        return blog.published_at or blog.author == self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(BlogDetailView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        services.create_blog_comment(form, self.request, self.object)
        return super(BlogDetailView, self).form_valid(form)

    def get_success_url(self):
        return reverse('app_blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(UserPassesTestMixin, generic.UpdateView):
    """Обновление информации записи блога"""
    template_name = 'app_blog/update_blog.html'
    form_class = forms.BlogForm
    queryset = models.Blog.objects.prefetch_related(
        Prefetch('images', queryset=models.BlogImage.objects.all(), to_attr='all_images'),
    )

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user

    def form_valid(self, form):
        services.create_update_blog(form, self.request)
        return super(BlogUpdateView, self).form_valid(form)


class BlogDeleteView(UserPassesTestMixin, generic.DeleteView):
    """Удаление записи блога"""
    model = models.Blog
    success_url = reverse_lazy('main_view')
    raise_exception = True

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user

    def get(self, request, *args, **kwargs):
        return redirect(reverse('main_view'))


class DeleteBlogImageView(UserPassesTestMixin, generic.DeleteView):
    """Удаление изображения, привязанного к блогу"""
    queryset = models.BlogImage.objects.select_related().all()
    raise_exception = True

    def test_func(self):
        image = self.get_object()
        return image.blog.author == self.request.user

    def get_success_url(self):
        return reverse('app_blog:blog_update', kwargs={'pk': self.object.blog.pk})

    def get(self, request, *args, **kwargs):
        return redirect(reverse('main_view'))


class UserBlogListView(CustomPaginateListView):
    """Список всех записей блога, конкретного пользователя"""
    template_name = 'app_blog/user_blog_list.html'
    context_object_name = 'blog_entries'
    paginate_cookie_name = 'blog_entries_per_page'
    queryset = models.Blog.objects.all().exclude(published_at__isnull=True).prefetch_related(
        Prefetch('images', queryset=models.BlogImage.objects.all(), to_attr='all_images'),
    )
    ordering = '-published_at'

    def get_queryset(self):
        queryset = super(UserBlogListView, self).get_queryset()
        queryset = queryset.filter(author__id=self.kwargs['pk'], author__slug=self.kwargs['slug'])
        return queryset


class BlogCreateFromFileView(LoginRequiredMixin, generic.FormView):
    """Создание записей блога из CSV файла"""
    template_name = 'app_blog/create_blog_from_file.html'
    form_class = forms.BlogEntriesFileForm

    def form_valid(self, form):
        services.create_blog_from_file(form, self.request)

        return super(BlogCreateFromFileView, self).form_valid(form)

    def get_success_url(self):
        url = reverse('app_blog:user_blog_entries', kwargs={'pk': self.request.user.pk,
                                                            'slug': self.request.user.slug, })
        return f'{url}?page=last'
