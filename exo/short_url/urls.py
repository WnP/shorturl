from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.create_short_url, name='create_short_url'),
    url(r'^url_list/$', views.url_list, name='url_list'),
    url(r'^(?P<pk>\d+)/$', views.redirect_to_long_url, name='redirect_to_long_url')
]
