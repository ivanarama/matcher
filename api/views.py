from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .matcher import match_legacy_record

@api_view(["POST"])
def match_view(request):
    legacy = request.data
    api_key = getattr(settings, "RAPIDAPI_KEY", None)
    result = match_legacy_record(legacy, api_key=api_key)
    return Response(result)