from django.views import generic


class MainView(generic.RedirectView):
    permanent = True
    pattern_name = 'app_users:user_list'


class CustomPaginateListView(generic.ListView):
    """
    Базовое представление c кастомной пагинацией.
    """
    paginate_by = 10
    paginate_cookie_name = 'objects_per_page'

    def get_paginate_by(self, queryset):
        try:
            objects_per_page = int(self.request.COOKIES.get(self.paginate_cookie_name))
            return objects_per_page
        except (ValueError, TypeError):
            pass

        return self.paginate_by

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        if page == 'last':
            page = paginator.num_pages
        page = paginator.get_page(page)

        return paginator, page, page.object_list, page.has_other_pages()
