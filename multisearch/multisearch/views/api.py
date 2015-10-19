"""
"""


import json
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from oauth2 import Client, Consumer


SUPPORTED_SITES = {
    "twitter": {},
    "wikipedia": {},
}

SUPPORTED_SITES_LIST = sorted(SUPPORTED_SITES.keys())

CONSUMER_KEY = "TzeYl9Ymn5bEFnt3gbQpZCjU3"

CONSUMER_SECRET = "0De4ArlxvMoSD24WaKJqmuasXa0fBruKbkPgJPHqj5jpocGbiN"

request_token_url = "https://api.twitter.com/oauth/request_token"

def test(request):
    return HttpResponse("Hello, World!")


def search(request, site=None):
    """."""
    
    # Check Preconditions
    required_get_parameters = {"term"}
    actual_get_parameters = set(request.GET.keys())
    missing_parameters = required_get_parameters - actual_get_parameters
    extra_parameters = actual_get_parameters - required_get_parameters

    if site not in SUPPORTED_SITES:
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
        
    consumer = Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    client = Client(consumer)
    url = "https://api.twitter.com/1.1/search/tweets.json?q=" + term
    resp, content = client.request(url, "GET")
    data = json.loads(content)
        
    return JsonResponse(data)


def sites(request):
    """."""
    return JsonResponse(SUPPORTED_SITES_LIST, safe=False)
    
    
def site(request, site=None):
    """."""
    # Check Precondition(s)
    if site not in SUPPORTED_SITES:
        return HttpResponseBadRequest(
            "Unknown site: {site}".format(site=site)
        )
            
    return JsonResponse(SUPPORTED_SITES[site])