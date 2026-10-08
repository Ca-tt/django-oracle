from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from store.models.store.product import Product


class NotFoundView(TemplateView):
    template_name = "store/pages/404.html"


class NotFoundPreview(TemplateView):
    template_name = "store/pages/404.html"


# not found 404
def not_found_404(request, exception):
    not_found_404_view = NotFoundView.as_view()
    return not_found_404_view(request, exception=exception)


# /search?q=
def search_results(request: HttpRequest) -> HttpResponse:
    results = None

    query = request.GET.get("q")
    if query:
        results = Product.objects.filter(title__icontains=query)
    else:
        results = Product.objects.none()

    return render(
        request, "store/pages/search_results.html", {"results": results, "query": query}
    )
