"""
WebSocket URL routing para la app cargas
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # WebSocket para rastreo GPS de un envío específico
    re_path(r'ws/tracking/(?P<envio_id>\w+)/$', consumers.GPSTrackingConsumer.as_asgi()),
]
