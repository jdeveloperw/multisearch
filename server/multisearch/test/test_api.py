"""."""


from collections import namedtuple
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from nose.tools import assert_equal

# The Software Under Test
from ..views.api import (
    sites,
    site
)


SiteTestCase = namedtuple("SitesTestCase", ["request", "expected"])

SITES_TEST_CASES = (
    SiteTestCase(request=None, expected=JsonResponse(settings.SUPPORTED_SITES, safe=False)),
)


def test_sites():
    """."""
    for test_case in SITES_TEST_CASES:
        yield check_sites, test_case.request, test_case.expected
    

def check_sites(request, expected):
    """."""
    actual = sites(request)
    assert_equal(type(expected), type(actual))
    assert_equal(expected.content, actual.content)
    
    
SiteTestCase = namedtuple("SiteTestCase", ["request", "site_id", "expected"])
    
SITE_TEST_CASES = (
    SiteTestCase(request=None, site_id=site["id"], expected=JsonResponse(site))
    for site in settings.SUPPORTED_SITES
)


def test_site():
    """."""
    for test_case in SITE_TEST_CASES:
        yield check_site, test_case.request, test_case.site_id, test_case.expected


def check_site(request, site_id, expected):
    actual = site(request, site_id=site_id)
    assert_equal(type(expected), type(actual))
    assert_equal(expected.content, actual.content)