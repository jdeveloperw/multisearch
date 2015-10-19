"""
"""


import json
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)


def test(request):
    return HttpResponse("Hello, World!")
    
    
def search_twitter(term):
    """."""
    
    url = settings.TWITTER_SEARCH_BASE_URL + term
    resp, content = settings.TWITTER_CLIENT.request(url, "GET")
    data = json.loads(content)
    return data
    
    
SITE_TO_SEARCH_FUNCTION = {
    "twitter": search_twitter,
}


def search(request, site=None):
    """."""
    
    # Check Preconditions
    required_get_parameters = {"term"}
    actual_get_parameters = set(request.GET.keys())
    missing_parameters = required_get_parameters - actual_get_parameters
    extra_parameters = actual_get_parameters - required_get_parameters

    if site not in settings.SUPPORTED_SITES:
        return HttpResponseBadRequest(
            "Unknown site: {site}".format(site=site)
        )
    elif missing_parameters:
        return HttpResponseBadRequest(
            "Missing these required parameters: {params}".format(params=missing_parameters)
        )
    elif extra_parameters:
        return HttpResponseBadRequest(
            "Unknown parameters: {params}".format(params=extra_parameters)
        )
        
    term = request.GET["term"]
    search_function = SITE_TO_SEARCH_FUNCTION[site]
    data = search_function(term)
    return JsonResponse(data)


def site(request):
    """."""
    return JsonResponse(SUPPORTED_SITES, safe=False)