from django.shortcuts import redirect, get_object_or_404
# from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# from django.template import Context

from django.views.generic import ListView
# from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.contrib import messages

from .models import URL
from .forms import URLForm

import pdb


class CreateShortURLView(FormView):
    # Voir https://hellowebbooks.com/news/introduction-to-class-based-views/
    # pour créer un context
    form_class = URLForm
    template_name = "short_url/create_short_url.html"

    def get_success_url(self):
        pdb.set_trace()
        return '{}?last_id={}'.format(reverse('url_list'), self.object.pk)

    def form_valid(self, form):
        obj = form.save()

        message = '<h1><a href="{1}">{1}</a></h1>' + \
            '<div class="{2}">' + \
            '{2}' + \
            '</div>' + \
            '<div class="{3}">' + \
            '{3}' + \
            '</div>' + \
            '<div class="{4}">' + \
            '{4}' + \
            '</div>' + \
            '<div class="{5}">' + \
            '{5}' + \
            '</div>' + \
            ''.format(obj.url_short,
                      obj.url_long,
                      obj.created_date,
                      obj.redirect_number)
        if obj.nickname is not None:
            message += '<div class="{1}">' + \
                '{1}' + \
                '</div>'.format(obj.nickname)
        messages.info(self.request, message)

        return super(CreateShortURLView, self).form_valid(form)


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


class URLListView(ListView):
    model = URL
    template_name = "short_url/url_list.html"

    def get_queryset(self):
        last_id = self.kwargs.get('last_id')
        if last_id is None:
            return URL.objects.all()
        else:
            return URL.objects.all().exclude(pk=last_id)


# def url_list(request):
#
#     return render(request, 'short_url/url_list.html', {
#         'urls': URL.objects.all()
#     })
