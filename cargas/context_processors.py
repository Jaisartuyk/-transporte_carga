"""
Context processors para hacer variables disponibles en todos los templates
"""
from django.conf import settings


def google_maps_api_key(request):
    """
    Hace la API Key de Google Maps disponible en todos los templates
    """
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
