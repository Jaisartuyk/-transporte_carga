# 🔄 FASE 3: WEBSOCKETS PARA TIEMPO REAL

## 🎯 **OBJETIVO:**

Implementar WebSockets para que el mapa de rastreo se actualice automáticamente en tiempo real sin recargar la página.

---

## 📊 **ESTADO ACTUAL vs OBJETIVO:**

### **Actual (Sin WebSockets):**
```
Conductor envía GPS → Se guarda en BD → Admin debe recargar página
```

### **Objetivo (Con WebSockets):**
```
Conductor envía GPS → WebSocket notifica → Mapa se actualiza automáticamente
```

---

## 🛠️ **TECNOLOGÍAS NECESARIAS:**

### **1. Django Channels**
```bash
pip install channels channels-redis daphne
```

### **2. Redis (Message Broker)**
```bash
# Opción 1: Docker (Recomendado)
docker run -d -p 6379:6379 redis

# Opción 2: Windows
# Descargar de: https://github.com/microsoftarchive/redis/releases
```

### **3. Configuración**
- ASGI application
- Channel layers
- WebSocket consumers
- Routing

---

## 📁 **ARCHIVOS A CREAR/MODIFICAR:**

```
transporte_carga/
├── asgi.py                    ✏️ Modificar
├── settings.py                ✏️ Modificar
├── routing.py                 ✅ Crear
└── cargas/
    ├── consumers.py           ✅ Crear
    ├── routing.py             ✅ Crear
    ├── api_views.py           ✏️ Modificar
    └── templates/
        └── envio_rastreo.html ✏️ Modificar
```

---

## 🔧 **IMPLEMENTACIÓN PASO A PASO:**

### **PASO 1: Instalar Dependencias**

```bash
pip install channels==4.0.0
pip install channels-redis==4.1.0
pip install daphne==4.0.0
```

### **PASO 2: Configurar settings.py**

```python
# Agregar a INSTALLED_APPS
INSTALLED_APPS = [
    'daphne',  # Debe estar PRIMERO
    'django.contrib.admin',
    # ... resto de apps
    'channels',
]

# Configurar ASGI
ASGI_APPLICATION = 'transporte_carga.asgi.application'

# Configurar Channel Layers
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### **PASO 3: Crear asgi.py**

```python
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cargas.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transporte_carga.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            cargas.routing.websocket_urlpatterns
        )
    ),
})
```

### **PASO 4: Crear cargas/consumers.py**

```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GPSTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.envio_id = self.scope['url_route']['kwargs']['envio_id']
        self.room_group_name = f'tracking_{self.envio_id}'

        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje del grupo
    async def gps_update(self, event):
        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'gps_update',
            'data': event['data']
        }))
```

### **PASO 5: Crear cargas/routing.py**

```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/tracking/(?P<envio_id>\w+)/$', consumers.GPSTrackingConsumer.as_asgi()),
]
```

### **PASO 6: Modificar api_views.py**

```python
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recibir_ubicacion(request):
    # ... código existente ...
    
    # Crear evento
    evento = EventoEnvio.objects.create(...)
    
    # NUEVO: Enviar por WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'tracking_{envio.id}',
        {
            'type': 'gps_update',
            'data': {
                'lat': float(lat),
                'lng': float(lng),
                'fecha': evento.fecha.isoformat(),
                'accuracy': accuracy,
                'speed': speed
            }
        }
    )
    
    return Response({...})
```

### **PASO 7: Actualizar envio_rastreo.html**

```javascript
// Conectar WebSocket
const envioId = {{ envio.id }};
const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
const wsUrl = `${wsScheme}://${window.location.host}/ws/tracking/${envioId}/`;
const socket = new WebSocket(wsUrl);

socket.onopen = function(e) {
    console.log('WebSocket conectado');
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'gps_update') {
        // Actualizar mapa en tiempo real
        actualizarMapaEnTiempoReal(data.data);
    }
};

socket.onclose = function(e) {
    console.log('WebSocket desconectado');
};

function actualizarMapaEnTiempoReal(coords) {
    // Agregar nuevo marcador
    const newMarker = new google.maps.Marker({
        position: { lat: coords.lat, lng: coords.lng },
        map: map,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 8,
            fillColor: '#667eea',
            fillOpacity: 1,
            strokeColor: '#ffffff',
            strokeWeight: 2
        }
    });
    
    // Actualizar polyline
    const path = pathPolyline.getPath();
    path.push(new google.maps.LatLng(coords.lat, coords.lng));
    
    // Centrar mapa
    map.setCenter({ lat: coords.lat, lng: coords.lng });
    
    // Mostrar notificación
    mostrarNotificacion('Nueva ubicación recibida');
}
```

---

## 🚀 **CÓMO EJECUTAR:**

### **1. Iniciar Redis**
```bash
# Docker
docker run -d -p 6379:6379 redis

# O Windows Redis
redis-server
```

### **2. Iniciar Django con Daphne**
```bash
# En lugar de: python manage.py runserver
# Usar:
daphne -b 0.0.0.0 -p 8000 transporte_carga.asgi:application
```

### **3. Probar**
```
1. Conductor abre /conductores/rastreo/
2. Admin abre /envios/15/rastrear/
3. Conductor inicia rastreo
4. Admin ve actualizaciones EN TIEMPO REAL sin recargar
```

---

## 🎯 **BENEFICIOS:**

```
✅ Actualizaciones instantáneas
✅ Sin recargar página
✅ Menor consumo de datos
✅ Mejor experiencia de usuario
✅ Escalable a múltiples usuarios
```

---

## 📊 **FLUJO COMPLETO:**

```
┌─────────────────────────────────────────────────┐
│ CONDUCTOR                                       │
│ /conductores/rastreo/                          │
│                                                 │
│ GPS obtiene ubicación                          │
│ ↓                                               │
│ Envía a /api/ubicacion/                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ SERVIDOR DJANGO                                 │
│                                                 │
│ 1. Guarda en EventoEnvio (BD)                  │
│ 2. Envía a Channel Layer (Redis)               │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ WEBSOCKET                                       │
│                                                 │
│ Notifica a todos los conectados                │
│ al grupo tracking_{envio_id}                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ ADMIN/CLIENTE                                   │
│ /envios/15/rastrear/                           │
│                                                 │
│ Recibe actualización por WebSocket             │
│ ↓                                               │
│ Actualiza mapa automáticamente                 │
│ ↓                                               │
│ Muestra notificación                           │
└─────────────────────────────────────────────────┘
```

---

## 🔐 **SEGURIDAD:**

### **Autenticación WebSocket:**
```python
class GPSTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Verificar autenticación
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        # Verificar permisos
        envio_id = self.scope['url_route']['kwargs']['envio_id']
        # Verificar que el usuario tenga acceso a este envío
        
        await self.accept()
```

---

## 💰 **COSTOS:**

### **Redis:**
```
- Desarrollo: GRATIS (local)
- Producción: 
  * Redis Cloud: $5-10/mes
  * AWS ElastiCache: $15-30/mes
  * Heroku Redis: $15/mes
```

---

## 🧪 **TESTING:**

### **Test 1: Conexión WebSocket**
```javascript
// En consola del navegador
const ws = new WebSocket('ws://localhost:8000/ws/tracking/15/');
ws.onopen = () => console.log('Conectado');
ws.onmessage = (e) => console.log('Mensaje:', e.data);
```

### **Test 2: Enviar Ubicación**
```bash
# Enviar ubicación por API
curl -X POST http://localhost:8000/api/ubicacion/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"lat": -2.9, "lng": -79.0}'
```

### **Test 3: Verificar Redis**
```bash
redis-cli
> KEYS *
> MONITOR
```

---

## ⚠️ **ALTERNATIVA SIN REDIS:**

Si no quieres usar Redis, puedes usar **In-Memory Channel Layer** (solo para desarrollo):

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

**Limitaciones:**
- ❌ No funciona con múltiples workers
- ❌ Se pierde al reiniciar
- ✅ Fácil para desarrollo

---

## 📈 **PRÓXIMOS PASOS:**

Después de WebSockets:
1. **Push Notifications** (Fase 4)
2. **Múltiples conductores en un mapa**
3. **Chat en tiempo real**
4. **Alertas instantáneas**

---

## 🎉 **RESULTADO FINAL:**

Con WebSockets tendrás:
- ✅ Mapa actualizado en tiempo real
- ✅ Sin recargar página
- ✅ Notificaciones instantáneas
- ✅ Múltiples usuarios viendo lo mismo
- ✅ Experiencia fluida y moderna

---

**¿Quieres que implemente WebSockets ahora?** 🚀
