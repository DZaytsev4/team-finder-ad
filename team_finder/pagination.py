from django.core.paginator import Paginator

DEFAULT_PER_PAGE = 12


def paginate(request, queryset, per_page: int = DEFAULT_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(request.GET.get("page"))

