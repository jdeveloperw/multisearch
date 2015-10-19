"""
"""


from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)


SUPPORTED_SITES = {
    "twitter": {},
    "wikipedia": {},
}

SUPPORTED_SITES_LIST = sorted(SUPPORTED_SITES.keys())


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
        
    return JsonResponse({})


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