from django import forms
from time import time
from hashlib import blake2b

from .models import URL


def random_url(*args, **kwargs):
    url_long = kwargs.get('url_long').encode()
    now = str(int(time()))[-8:].encode()

    return blake2b(key=url_long[:64], digest_size=4, salt=now).hexdigest()


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ('url_long', 'nickname')

    def save(self, *args, **kwargs):
        created = False

        while not created:
            url_short = random_url(
                url_long=self.cleaned_data.get('url_long')
            )
            obj, created = URL.objects.get_or_create(
                url_long=self.cleaned_data.get('url_long'),
                nickname=self.cleaned_data.get('nickname'),
                url_short=url_short,
            )

        return
