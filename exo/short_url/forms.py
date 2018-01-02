from django import forms
from django.db import IntegrityError
from time import time
from hashlib import blake2b

from .models import URL


def get_hash(*args, **kwargs):
    """
    get_hash take an url in 'url_long' with optionnal 'rand' (it's a bool).
    if rand is true, it introduce some salt in blake2b.
    It return a hash string
    """
    url_long = kwargs.get('url_long').encode()
    salt = kwargs.get('rand', False) and str(int(time()))[-8:].encode() or b''

    return blake2b(key=url_long[:64], digest_size=4, salt=salt).hexdigest()


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ('url_long', 'nickname')

    def __init__(self, *args, **kwargs):
        # overloading init method to be able to set a custom hash func
        # useful for testing
        self.get_hash = kwargs.pop('hash_func', get_hash)
        return super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        url_long = self.cleaned_data.get('url_long')

        try:
            url_short = self.get_hash(url_long=url_long)
            url, _ = URL.objects.get_or_create(
                url_long=self.cleaned_data.get('url_long'),
                nickname=self.cleaned_data.get('nickname'),
                url_short=url_short,
            )
            return url
        except IntegrityError:
            url_short = self.get_hash(url_long=url_long, rand=True)
            url, _ = URL.objects.get_or_create(
                url_long=self.cleaned_data.get('url_long'),
                nickname=self.cleaned_data.get('nickname'),
                url_short=url_short,
            )
            return url
