from django.conf import settings


def business_info(request):
    """Makes BUSINESS dict available in every template as `business`."""
    return {'business': settings.BUSINESS}
