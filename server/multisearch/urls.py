"""multisearch URL Configuration

Configure URL for endpoints:
/site/
/site/:site_id/
/search/:site_id?term=foo
"""


from django.conf.urls import url
from .views.api import (
    search,
    sites,
    site,
)


urlpatterns = [
    url(r'^search/(?P<site_id>\w+).*$', search, name="search"),
    url(r'^site/$', sites, name="sites"),
    url(r'^site/(?P<site_id>\w+)/$', site, name="site"),
]