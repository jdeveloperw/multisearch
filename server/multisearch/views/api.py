"""API endpoints for multisearch"""


import json
import requests
from django.conf import settings
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)


def search_twitter(term):
    """Query the Twitter API for term and return statuses that match
    Returns a list of dictionaries.
    Each dictionary has these keys: title, description, url"""
    
    url = settings.TWITTER_SEARCH_BASE_URL + term
    resp, content = settings.TWITTER_CLIENT.request(url, method="GET")
    raw_data = json.loads(content)
    data = [
        {"title": "", "description": status["text"], "url": "https://twitter.com/statuses/{id}".format(id=status["id"])}
        for status in raw_data["statuses"]
    ]
    return data
    
    
def search_wikipedia(term):
    """Query the Wikipedia API for the term.
    Returns a list of dictionaries.
    Each dictionary has these keys: title, description, url"""
    
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


def search(request, site_id=None):
    """Query the API given by site_id for the term in the request.
    Returns a list of dictionaries.
    Each dictionary has these keys: title, description, url"""
    
    # Check Preconditions
    required_get_parameters = {"term"}
    actual_get_parameters = set(request.GET.keys())
    missing_parameters = required_get_parameters - actual_get_parameters
    extra_parameters = actual_get_parameters - required_get_parameters

    if site_id not in settings.SUPPORTED_SITE_IDS:
        return HttpResponseBadRequest(
            "Unknown site: {site_id}".format(site_id=site_id)
        )
    elif missing_parameters:
        return HttpResponseBadRequest(
            "Missing required parameters: {params}".format(params=", ".join(missing_parameters))
        )
    elif extra_parameters:
        return HttpResponseBadRequest(
            "Unknown parameters: {params}".format(params=", ".join(extra_parameters))
        )
        
    term = request.GET["term"]
    search_function = SITE_TO_SEARCH_FUNCTION[site_id]
    data = search_function(term)
    return JsonResponse(data, safe=False)


def sites(request):
    """Return a list of all sites that are supported.
    Each element in the list is a dict containing with keys: id, label"""
    
    return JsonResponse(settings.SUPPORTED_SITES, safe=False)


def site(request, site_id=None):
    """Return a dict for the given site_id containing with keys: id, label"""
    
    # Check Preconditions
    if site_id not in settings.SUPPORTED_SITE_IDS:
        return HttpResponseBadRequest(
            "Unknown site: {site_id}".format(site_id=site_id)
        )
    
    return JsonResponse(settings.SITE_ID_TO_SITE[site_id], safe=False)