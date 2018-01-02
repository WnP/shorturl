from django.shortcuts import render, redirect, get_object_or_404

from .models import URL
from .forms import URLForm


def create_short_url(request):
    form = URLForm()
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if obj is None:
                return render(request, 'short_url/url_list.html', {
                    'error': True,
                })
            else:
                urls = URL.objects.all().order_by('created_date')[1:]

                return render(request, 'short_url/url_list.html', {
                    'latest': obj,
                    'urls': urls,
                    'error': False,
                })

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
