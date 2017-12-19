from django.shortcuts import render, redirect, get_object_or_404

from .models import URL
from .forms import URLForm

# import pdb

#
# def random_url(*args, **kwargs):
#     url_long = kwargs.get('url_long').encode()
#     now = str(int(time()))[-8:].encode()
#
#     return blake2s(key=url_long, digest_size=4, salt=now).hexdigest()


def create_short_url(request):
    form = URLForm(request.POST)
    # pdb.set_trace()
    if form.is_valid():
        form.save()

        return redirect('url_list')

    return render(request, 'short_url/create_short_url.html', {'form': form})


def redirect_to_long_url(request, pk):
    url = get_object_or_404(URL, pk=pk)
    url.redirect_number += 1
    url.save()

    return redirect(url.url_long)


def url_list(request):
    urls = URL.objects.all().order_by('created_date')

    return render(request, 'short_url/url_list.html', {'urls': urls})
