"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cargas.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicializar Django ASGI application temprano para asegurar que AppRegistry esté poblado
# antes de importar código que pueda importar modelos ORM.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            cargas.routing.websocket_urlpatterns
        )
    ),
})
