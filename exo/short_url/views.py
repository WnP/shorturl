from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError

from .models import URL
from .forms import URLForm


def create_short_url(request):
    form = URLForm()
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if obj:
                return render(
                    request,
                    'short_url/url_list.html',
                    {'urls': {obj}}
                )
            else:
                return render(
                    request,
                    'short_url/create_error.html',
                    {
                        'error':
                        "We can't create a short url. Please try in few minutes"
                    }
                )

    return render(request, 'short_url/create_short_url.html', {'form': form})


def create_error(request):
    return render(request, 'short_url/create_error.html')


def redirect_to_long_url(request, pk):
    url = get_object_or_404(URL, pk=pk)
    url.redirect_number += 1
    url.save()

    return redirect(url.url_long)


def url_list(request):
    urls = URL.objects.all().order_by('created_date')

    return render(request, 'short_url/url_list.html', {'urls': urls})
