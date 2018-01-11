from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.contrib import messages

from .models import URL
from .forms import URLForm


class CreateShortURLView(FormView):
    # Voir https://hellowebbooks.com/news/introduction-to-class-based-views/
    # pour créer un context
    form_class = URLForm
    template_name = "short_url/create_short_url.html"

    def get_success_url(self):
        return '{}?last_created_id={}'.format(
            reverse('url_list'),
            self.last_created_id
        )

    def form_valid(self, form):
        obj = form.save()

        self.last_created_id = obj.id

        message = '<h1><a href="{}">{}</a></h1>' \
            '<div class="url_long">' \
            '{}' \
            '</div>' \
            ''.format(obj.id,
                      obj.url_short,
                      obj.url_long,)
        if obj.nickname is not None:
            message += '<div class="{1}">' \
                '{1}' \
                '</div>'.format(obj.nickname)
        messages.info(self.request, message)

        return super(CreateShortURLView, self).form_valid(form)


class RedirectToLongURLView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        url = get_object_or_404(URL, pk=kwargs['pk'])
        url.redirect_number += 1
        url.save()

        return url.url_long


class URLListView(ListView):
    model = URL
    template_name = "short_url/url_list.html"
    context_object_name = "urls"

    def get_queryset(self):
        last_created_id = self.kwargs.get('last_created_id')
        if last_created_id is None:
            return URL.objects.all()
        else:
            return URL.objects.all().exclude(pk=last_created_id)
