from django.shortcuts import render, redirect, get_object_or_404

# from django.template import Context

# from django.views.generic import ListView
# from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from .models import URL
from .forms import URLForm


class CreateShortURLView(FormView):
    # Voir https://hellowebbooks.com/news/introduction-to-class-based-views/
    # pour créer un context
    form_class = URLForm
    template_name = "short_url/create_short_url.html"

    def form_valid(self, form):
        obj = form.save()
        return render(self.request, 'short_url/url_list.html', {
            'error': obj is None,
            'latest': obj,
            'urls': URL.objects.all().exclude(pk=obj.pk)
        })


# class RedirectToLongURLView(RedirectView):
#     permanent = False
#
#     def get_redirect_url(self, *args, **kwargs):
#         url = get_object_or_404(URL, pk=kwargs['pk'])
#         url.redirect_number += 1
#         url.save()
#         # self.kwargs['url'] = url.url_long
#
#         return super(RedirectToLongURLView, self).get_redirect_url(*args,
#                                                                    **kwargs)


def redirect_to_long_url(request, pk):
    url = get_object_or_404(URL, pk=pk)
    url.redirect_number += 1
    url.save()

    return redirect(url.url_long)


# class URLListView(ListView):
#     model = URL
#     template_name = "short_url/url_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(URLList, self).get_context_data(**kwargs)
#         context['error'] = …
#         return context


def url_list(request):

    return render(request, 'short_url/url_list.html', {
        'urls': URL.objects.all()
    })
