from django.conf.urls import url
from short_url.views import URLListView, CreateShortURLView, \
    RedirectToLongURLView

urlpatterns = [
    url(r'^$', CreateShortURLView.as_view(), name='create_short_url'),
    url(r'^url_list/$', URLListView.as_view(), name='url_list'),
    url(r'^url_list/(?P<pk>\d+)/$', RedirectToLongURLView.as_view(),
        name='redirect_to_long_url')
]
