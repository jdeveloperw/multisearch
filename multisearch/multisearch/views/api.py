"""
"""


from django.http import HttpResponse, HttpResponseBadRequest


def test(request):
    return HttpResponse("Hello, World!")


def search(request):
    required_get_parameters = {"term", "sites"}
    actual_get_parameters = set(request.GET.keys())
    missing_parameters = required_get_parameters - actual_get_parameters
    extra_parameters = actual_get_parameters - required_get_parameters

    if missing_parameters:
        return HttpResponseBadRequest(
            "Missing these required parameters: {params}".format(params=missing_parameters)
        )
    elif extra_parameters:
        return HttpResponseBadRequest(
            "Unknown parameters: {params}".format(params=extra_parameters)
        )
    else:
        return HttpResponse("Searching...")


def sites(request):
    return HttpResponse("Sites")
