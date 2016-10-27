from urlparse import urlparse

from django.middleware.clickjacking import XFrameOptionsMiddleware
from django.conf import settings

class ExemptFrameOptionsMiddleware(XFrameOptionsMiddleware):
    """
    By default, XFrameOptionsMiddleware prevents non-originating IP addresses from loading our content 
    in iFrame. This middleware exempts our authorized servers from such rule.
    """
    def get_xframe_options_value(self, request, response):
        referer = request.META.get('HTTP_REFERER', None)
        if referer and urlparse(referer).hostname in settings.XFRAME_EXEMPT_IPS:
            return 'ALLOWALL' # non standard, equivalent to omitting
        return super(ExemptFrameOptionsMiddleware, self).get_xframe_options_value(request, response)
