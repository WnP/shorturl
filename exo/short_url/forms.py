from django import forms
from django.core.exceptions import ValidationError
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
    rand = kwargs.get('rand', False)

    if rand:
        now = str(int(time()))[-8:].encode()
        return blake2b(key=url_long[:64], digest_size=4, salt=now).hexdigest()
    else:
        return blake2b(key=url_long[:64], digest_size=4).hexdigest()

import pdb

class URLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ('url_long', 'nickname')

    def save(self, *args, **kwargs):
        for i in range(4):
            # pdb.set_trace()

            url_short = get_hash(url_long=self.cleaned_data.get('url_long'))
            _, created = URL.objects.get_or_create(
                url_long=self.cleaned_data.get('url_long'),
                nickname=self.cleaned_data.get('nickname'),
                url_short=url_short,
            )
            if created:
                return
        else:
            raise forms.ValidationError(_('Unable to create an short url'))


    # def save_bis(self, *args, **kwargs):
    #     url_short = get_hash(url_long=self.cleaned_data.get('url_long'))
    #     _, created = URL.objects.get_or_create(
    #         url_long=self.cleaned_data.get('url_long'),
    #         nickname=self.cleaned_data.get('nickname'),
    #         url_short=url_short,
    #     )
    #     if created:
    #         return
    #
    #     url_short = get_hash(url_long=self.cleaned_data.get('url_long'),
    #                          rand=True,)
    #     _, created = URL.objects.get_or_create(
    #         url_long=self.cleaned_data.get('url_long'),
    #         nickname=self.cleaned_data.get('nickname'),
    #         url_short=url_short,
    #     )
    #     if created:
    #         return
    #
    #     raise forms.ValidationError(_('Unable to create an short url'))
