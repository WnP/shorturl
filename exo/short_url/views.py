from django.shortcuts import render, redirect, get_object_or_404

from .models import URL
from .forms import URLForm


def create_short_url(request):
    form = URLForm()
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return render(request, 'short_url/url_list.html', {
                'error': obj is None,
                'latest': obj,
                'urls': URL.objects.all().exclude(pk=obj.pk)
            })

    return render(request, 'short_url/create_short_url.html', {'form': form})


def redirect_to_long_url(request, pk):
    url = get_object_or_404(URL, pk=pk)
    url.redirect_number += 1
    url.save()

    return redirect(url.url_long)


def url_list(request):

    return render(request, 'short_url/url_list.html', {
        'urls': URL.objects.all()
    })
