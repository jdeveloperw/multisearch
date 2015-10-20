"""
"""


import json
import requests
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
    raw_data = json.loads(content)
    data = [
        {"title": "", "description": status["text"], "url": "https://twitter.com/statuses/{id}".format(id=status["id"])}
        for status in raw_data["statuses"]
    ]
    return data
    
    
def search_wikipedia(term):
    """."""
    url = "https://en.wikipedia.org/w/api.php?action=opensearch&search=" + term
    response = requests.get(url)
    raw_data = response.json()
    
    search_term = raw_data[0]
    titles = raw_data[1]
    descriptions = raw_data[2]
    urls = raw_data[3]
    
    data = [
        {"title": title, "description": description, "url": url}
        for title, description, url in zip(titles, descriptions, urls)
    ]
    return data
    
SITE_TO_SEARCH_FUNCTION = {
    "twitter": search_twitter,
    "wikipedia": search_wikipedia,
}


def search(request, site=None):
    """."""
    
    # Check Preconditions
    required_get_parameters = {"term"}
    actual_get_parameters = set(request.GET.keys())
    missing_parameters = required_get_parameters - actual_get_parameters
    extra_parameters = actual_get_parameters - required_get_parameters

    if site not in settings.SUPPORTED_SITE_IDS:
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
    return JsonResponse(data, safe=False)


def site(request):
    """."""
    return JsonResponse(settings.SUPPORTED_SITES, safe=False)