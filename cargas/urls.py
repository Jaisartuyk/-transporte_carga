from django.urls import path
from django.shortcuts import redirect
from . import views
from . import api_views

def redirect_to_dashboard(request):
    return redirect('dashboard')

urlpatterns = [
    path("", redirect_to_dashboard, name="home"),
    path("login/", views.user_login, name="user_login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/conductor/", views.dashboard_conductor, name="dashboard_conductor"),
    path("dashboard/cliente/", views.dashboard_cliente, name="dashboard_cliente"),
    path("dashboard/react/", views.dashboard_react, name="dashboard_react"),
    path("envios/", views.envios_list, name="envios_list"),
    path("vehiculos/", views.vehiculos_list, name="vehiculos_list"),
    path("alertas/", views.alertas_list, name="alertas_list"),
    path("alertas/<int:alerta_id>/", views.alerta_detalle, name="alerta_detalle"),
    path("alertas/<int:alerta_id>/atender/", views.atender_alerta, name="atender_alerta"),
    path("conductores/", views.conductores_list, name="conductores_list"),
    path("conductores/nuevo/", views.crear_conductor, name="crear_conductor"),
    path("conductores/rastreo/", views.conductor_rastreo, name="conductor_rastreo"),
    path("conductores/<int:conductor_id>/", views.conductor_detalle, name="conductor_detalle"),
    path("conductores/<int:conductor_id>/editar/", views.editar_conductor, name="editar_conductor"),

    path("vehiculos/nuevo/", views.crear_vehiculo, name="crear_vehiculo"),
    path("vehiculos/<int:vehiculo_id>/", views.vehiculo_detalle, name="vehiculo_detalle"),
    path("vehiculos/<int:vehiculo_id>/editar/", views.editar_vehiculo, name="editar_vehiculo"),
    path("vehiculos/<int:vehiculo_id>/ubicacion/", views.vehiculo_ubicacion, name="vehiculo_ubicacion"),

    path("envios/nuevo/", views.crear_envio, name="crear_envio"),
    path("envios/<int:envio_id>/", views.envio_detalle, name="envio_detalle"),
    path("envios/<int:envio_id>/rastrear/", views.rastrear_envio, name="rastrear_envio"),
    path("envios/<int:envio_id>/editar/", views.editar_envio, name="editar_envio"),
    
    # Autenticación
    path("logout/", views.logout_view, name="logout"),
    
    # API para GPS Tracking
    path("api/ubicacion/", api_views.recibir_ubicacion, name="api_ubicacion"),
    path("api/ubicacion/sync/", api_views.sincronizar_ubicaciones, name="api_ubicacion_sync"),
]
