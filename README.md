# 🚛 CargoTrack Pro - Sistema de Gestión de Transporte de Carga

![Django](https://img.shields.io/badge/Django-5.2.6-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![PWA](https://img.shields.io/badge/PWA-Ready-purple)

Sistema completo de gestión y rastreo de transporte de carga con GPS en tiempo real, desarrollado con Django y tecnologías web modernas.

## 🎯 Características Principales

### ✅ Gestión Completa
- **Multi-rol**: Admin, Conductor, Cliente
- **Dashboards personalizados** por rol
- **CRUD completo** de envíos, vehículos y conductores
- **Sistema de alertas** (robo, accidente, desvío)
- **Autenticación segura** con permisos por rol

### 📍 Rastreo GPS
- **Tiempo real** con WebSockets
- **Rastreo en segundo plano** en móviles
- **Google Maps** integrado
- **Actualización automática** cada 30 segundos
- **Historial de rutas** con polyline

### 📱 PWA (Progressive Web App)
- **Instalable** en dispositivos móviles
- **Funciona offline** con Service Worker
- **Caché inteligente** de recursos
- **Background Sync** para sincronización
- **Wake Lock API** para rastreo continuo

### 🔔 Notificaciones
- **Notificaciones push** (próximamente)
- **Alertas en tiempo real**
- **Indicadores visuales** de estado

### 🎨 Interfaz Moderna
- **Bootstrap 5.3** con diseño responsive
- **Gradientes y animaciones** suaves
- **Menú adaptativo** según rol
- **Navbar personalizado** con avatar
- **Iconos Bootstrap** en toda la app

## 🚀 Tecnologías Utilizadas

### Backend
- **Django 5.2.6** - Framework web
- **Django REST Framework** - API REST
- **Django Channels 4.2.2** - WebSockets
- **SQLite3** - Base de datos

### Frontend
- **Bootstrap 5.3** - Framework CSS
- **Bootstrap Icons** - Iconografía
- **Chart.js** - Gráficos
- **Google Maps API** - Mapas
- **Vanilla JavaScript** - Lógica del cliente

### PWA & APIs
- **Service Worker** - Caché offline
- **Web App Manifest** - Instalación PWA
- **Geolocation API** - GPS
- **Wake Lock API** - Rastreo continuo
- **Background Sync API** - Sincronización
- **Notifications API** - Notificaciones

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/transporte_carga.git
cd transporte_carga
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Aplicar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Recolectar archivos estáticos**
```bash
python manage.py collectstatic
```

8. **Ejecutar servidor**

Sin WebSockets:
```bash
python manage.py runserver
```

Con WebSockets:
```bash
daphne -b 127.0.0.1 -p 8000 core.asgi:application
```

9. **Acceder a la aplicación**
```
http://127.0.0.1:8000/
```

## 👥 Roles y Permisos

### 👨‍💼 Administrador
- ✅ Acceso completo al sistema
- ✅ Gestión de envíos, vehículos y conductores
- ✅ Ver todas las estadísticas
- ✅ Panel de administración Django
- ✅ Rastreo GPS de todos los vehículos

### 🚛 Conductor
- ✅ Dashboard personalizado
- ✅ Ver sus envíos asignados
- ✅ Panel de rastreo GPS
- ✅ Enviar ubicación en tiempo real
- ✅ Ver su vehículo
- ❌ No ve otros conductores

### 👤 Cliente
- ✅ Dashboard personalizado
- ✅ Ver solo SUS envíos
- ✅ Rastrear sus envíos en tiempo real
- ✅ Ver alertas de sus envíos
- ❌ No ve vehículos ni conductores
- ❌ No accede a panel GPS

## 📱 Usar como PWA

### Android
1. Abrir en Chrome
2. Menú → "Agregar a pantalla de inicio"
3. Confirmar instalación
4. Abrir desde icono

### iOS
1. Abrir en Safari
2. Compartir → "Agregar a pantalla de inicio"
3. Confirmar
4. Abrir desde icono

## 🗺️ Configuración de Google Maps

1. Obtener API Key en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilitar APIs:
   - Maps JavaScript API
   - Geocoding API
   - Places API
3. Reemplazar la API Key en los templates:
   - `conductor_rastreo.html`
   - `envio_rastreo.html`
   - `vehiculo_ubicacion.html`

```html
<script src="https://maps.googleapis.com/maps/api/js?key=TU_API_KEY&libraries=places"></script>
```

## 📁 Estructura del Proyecto

```
transporte_carga/
├── cargas/                 # App principal
│   ├── migrations/         # Migraciones de BD
│   ├── static/            # Archivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   │   ├── background-location.js
│   │   │   ├── service-worker.js
│   │   │   └── pwa-install.js
│   │   └── icons/         # Iconos PWA
│   ├── templates/         # Templates HTML
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas
│   ├── urls.py            # URLs
│   ├── consumers.py       # WebSocket consumers
│   └── routing.py         # WebSocket routing
├── core/                  # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py           # ASGI para WebSockets
│   └── wsgi.py
├── media/                 # Archivos subidos
├── static/                # Archivos estáticos globales
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## 🔧 Configuración

### Variables de Entorno (Opcional)
Crear archivo `.env` en la raíz:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
GOOGLE_MAPS_API_KEY=tu-api-key-aqui
```

### Configuración de WebSockets
En `settings.py`:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
```

Para producción, usar Redis:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

## 📊 Modelos de Datos

### Usuario
- Roles: admin, conductor, cliente
- Campos: username, email, teléfono, documento

### Vehículo
- Placa, marca, modelo, año
- Capacidad, estado
- Conductor asignado

### Envío
- Número de guía (auto-generado)
- Cliente, vehículo
- Origen, destino
- Estados: pendiente, en_ruta, entregado, incidencia

### EventoEnvio
- Seguimiento GPS
- Ubicación, coordenadas
- Velocidad, precisión

### Alerta
- Tipos: robo, accidente, desvío, retraso
- Envío asociado
- Estado de atención

## 🚀 Despliegue

### Heroku
```bash
# Instalar Heroku CLI
heroku login
heroku create tu-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Railway
1. Conectar repositorio GitHub
2. Configurar variables de entorno
3. Deploy automático

### PythonAnywhere
1. Subir código
2. Configurar virtualenv
3. Configurar WSGI
4. Recargar aplicación

## 📝 Documentación Adicional

- [Manual del Cliente](MANUAL_CLIENTE.md)
- [Sistema Completo](SISTEMA_COMPLETO_FINAL.md)
- [Rastreo en Segundo Plano](RASTREO_SEGUNDO_PLANO.md)
- [Autenticación](AUTENTICACION_COMPLETA.md)
- [Menú por Rol](MENU_POR_ROL.md)

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@TU_USUARIO](https://github.com/TU_USUARIO)
- Email: tu-email@ejemplo.com

## 🙏 Agradecimientos

- Django Framework
- Bootstrap Team
- Google Maps Platform
- Comunidad Open Source

## 📞 Soporte

Para soporte, email a soporte@cargotrack.ec o únete a nuestro canal de Slack.

---

**⭐ Si te gusta este proyecto, dale una estrella en GitHub!**

Hecho con ❤️ en Ecuador 🇪🇨
