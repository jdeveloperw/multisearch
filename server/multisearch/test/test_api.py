"""Test API endpoints for multisearch"""


from collections import namedtuple
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.test import RequestFactory
from nose.tools import assert_equal

# The Software Under Test
from ..views.api import (
    search,
    sites,
    site
)


# Test Case definition for /site/
SiteTestCase = namedtuple("SitesTestCase", ["request", "expected"])

# Test Cases for /site/
SITES_TEST_CASES = (
    SiteTestCase(request=None, expected=JsonResponse(settings.SUPPORTED_SITES, safe=False)),
)


def test_sites():
    """Test handler for /site/:site_id/ endpoint"""
    for test_case in SITES_TEST_CASES:
        yield check_sites, test_case.request, test_case.expected
    

def check_sites(request, expected):
    """Check that response from /site/ matches expected"""
    actual = sites(request)
    assert_equal(type(expected), type(actual))
    assert_equal(expected.content, actual.content)
    
    
# Test Case definition for /site/:site_id/
SiteTestCase = namedtuple("SiteTestCase", ["request", "site_id", "expected"])
    
# Test Cases for /site/:site_id/
SITE_TEST_CASES = (
    SiteTestCase(request=None, site_id=site["id"], expected=JsonResponse(site))
    for site in settings.SUPPORTED_SITES
)


def test_site():
    """Test handler for /site/:site_id/ endpoint"""
    for test_case in SITE_TEST_CASES:
        yield check_site, test_case.request, test_case.site_id, test_case.expected


def check_site(request, site_id, expected):
    """Check that response from /site/:site_id/ matches expected"""
    actual = site(request, site_id=site_id)
    assert_equal(type(expected), type(actual))
    assert_equal(expected.content, actual.content)

# Test Case definition for /site/
SiteTestCase = namedtuple("SitesTestCase", ["request", "expected"])

# Test Cases for /site/
SITES_TEST_CASES = (
    SiteTestCase(request=None, expected=JsonResponse(settings.SUPPORTED_SITES, safe=False)),
)


def test_sites():
    """Test handler for /site/:site_id/ endpoint"""
    for test_case in SITES_TEST_CASES:
        yield check_sites, test_case.request, test_case.expected
    

def check_sites(request, expected):
    """Check that response from /site/ matches expected"""
    actual = sites(request)
    compare_responses(expected, actual)
    
    
# Test Case definition for /site/:site_id/
SiteTestCase = namedtuple("SiteTestCase", ["request", "site_id", "expected"])
    
# Test Cases for /site/:site_id/
SITE_TEST_CASES = (
    SiteTestCase(request=None, site_id=site["id"], expected=JsonResponse(site))
    for site in settings.SUPPORTED_SITES
)


def test_site():
    """Test handler for /site/:site_id/ endpoint"""
    for test_case in SITE_TEST_CASES:
        yield check_site, test_case.request, test_case.site_id, test_case.expected


def check_site(request, site_id, expected):
    """Check that response from /site/:site_id/ matches expected"""
    actual = site(request, site_id=site_id)
    compare_responses(expected, actual)
    
    
# Test Case definition for /search
SearchTestCase = namedtuple("SearchTestCase", ["request", "site_id", "expected"])

# Test Cases for /search
SEARCH_TEST_CASES = (
    # Unknown site
    SiteTestCase(request=RequestFactory().get("/search/foo"),
                 site_id="foo",
                 expected=HttpResponseBadRequest("Unknown site: foo")),
    # No search term
    SiteTestCase(request=RequestFactory().get("/search/wikipedia"),
                 site_id="wikipedia",
                 expected=HttpResponseBadRequest("Missing required parameters: term")),
    # Extra parameters
    SiteTestCase(request=RequestFactory().get("/search/wikipedia?term=foo&fiz=buz"),
                 site_id="wikipedia",
                 expected=HttpResponseBadRequest("Unknown parameters: fiz")),
)


def test_search():
    """Test handler for /search endpoint"""
    for test_case in SEARCH_TEST_CASES:
        yield check_search, test_case.request, test_case.site_id, test_case.expected


def check_search(request, site_id, expected):
    """Check that response from /search matches expected"""
    actual = search(request, site_id=site_id)
    compare_responses(expected, actual)
    
    
def compare_responses(expected, actual):
    """Check that actual response matches expected response"""
    assert_equal(type(expected), type(actual))
    assert_equal(expected.status_code, actual.status_code)
    assert_equal(expected.content, actual.content)