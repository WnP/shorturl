from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import URL
from .forms import URLForm

# import pdb


def create_short_url(request):
    form = URLForm(request.POST)
    # pdb.set_trace()
    if form.is_valid():
        try:
            form.save()
        except ValidationError as e:
            return render(request,
                          'short_url/create_error.html',
                          {'error': e.strerror},
                         )

        else:
            return redirect('url_list')

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
