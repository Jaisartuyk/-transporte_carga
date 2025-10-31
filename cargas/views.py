from rest_framework import viewsets, permissions
from .models import Envio, EventoEnvio, Alerta, Vehiculo
from .serializers import EnvioSerializer, EventoEnvioSerializer, AlertaSerializer, VehiculoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ConductorForm, VehiculoForm, EnvioForm
from django.db.models import Count
from .models import Usuario, Envio, Vehiculo, Alerta
from django.utils.timezone import now
from django.db.models.functions import TruncMonth


# ✅ Cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente")
    return redirect('user_login')


# ✅ Vista de login personalizada
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login as auth_login
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Bienvenido, {user.get_full_name()}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    
    return render(request, 'login.html')

# 🔹 Envíos (visible para clientes y admin)
class EnvioViewSet(viewsets.ModelViewSet):
    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer
    permission_classes = [permissions.IsAuthenticated]

# 🔹 Eventos (chofer registra ubicación)
class EventoEnvioViewSet(viewsets.ModelViewSet):
    queryset = EventoEnvio.objects.all()
    serializer_class = EventoEnvioSerializer
    permission_classes = [permissions.IsAuthenticated]

# 🔹 Alertas (chofer o sistema)
class AlertaViewSet(viewsets.ModelViewSet):
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    permission_classes = [permissions.IsAuthenticated]

# 🔹 Vehículos (solo admin)
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAdminUser]



@login_required
def dashboard(request):
    # Redirigir según el rol del usuario
    if request.user.is_authenticated:
        if request.user.rol == 'conductor':
            return redirect('dashboard_conductor')
        elif request.user.rol == 'cliente':
            return redirect('dashboard_cliente')
    
    # Dashboard para administradores
    # 🔹 Contadores principales
    envios_count = Envio.objects.count()
    vehiculos_count = Vehiculo.objects.count()
    conductores_count = Usuario.objects.filter(rol="conductor").count()
    alertas_count = Alerta.objects.count()

    # 🔹 Envíos por mes (últimos 6 meses)
    envios_por_mes = (
        Envio.objects
        .annotate(mes=TruncMonth("fecha_creacion"))
        .values("mes")
        .annotate(total=Count("id"))
        .order_by("mes")
    )
    meses = [e["mes"].strftime("%b %Y") for e in envios_por_mes]
    envios_data = [e["total"] for e in envios_por_mes]

    # 🔹 Estados de envíos
    estados_envios = [
        Envio.objects.filter(estado="pendiente").count(),
        Envio.objects.filter(estado="en_ruta").count(),
        Envio.objects.filter(estado="entregado").count(),
        Envio.objects.filter(estado="incidencia").count(),
    ]

    # 🔹 Estado de vehículos (ajustado para 3 categorías)
    vehiculos_disponibles = Vehiculo.objects.filter(estado="disponible").count()
    vehiculos_en_ruta = Vehiculo.objects.filter(estado="en_ruta").count()
    vehiculos_mantenimiento = Vehiculo.objects.filter(estado="mantenimiento").count()
    
    vehiculos_estado = [vehiculos_disponibles, vehiculos_en_ruta, vehiculos_mantenimiento]
    
    # Calcular porcentajes para la flota
    total_vehiculos = vehiculos_count if vehiculos_count > 0 else 1
    vehiculos_disponibles_pct = round((vehiculos_disponibles / total_vehiculos) * 100)
    vehiculos_en_ruta_pct = round((vehiculos_en_ruta / total_vehiculos) * 100)
    vehiculos_mantenimiento_pct = round((vehiculos_mantenimiento / total_vehiculos) * 100)

    # 🔹 Últimos registros con select_related para optimizar consultas
    ultimos_conductores = Usuario.objects.filter(rol="conductor").order_by("-id")[:5]
    ultimos_vehiculos = Vehiculo.objects.select_related('conductor').order_by("-id")[:5]
    ultimos_envios = Envio.objects.select_related('cliente', 'vehiculo').order_by("-fecha_creacion")[:5]
    ultimas_alertas = Alerta.objects.select_related('envio').order_by("-fecha")[:5]
    
    # Contadores para sidebar
    envios_activos = Envio.objects.filter(estado__in=['pendiente', 'en_ruta']).count()
    alertas_pendientes = Alerta.objects.filter(atendida=False).count()

    context = {
        "envios_count": envios_count,
        "vehiculos_count": vehiculos_count,
        "conductores_count": conductores_count,
        "alertas_count": alertas_count,
        "meses": meses,
        "envios_data": envios_data,
        "estados_envios": estados_envios,
        "vehiculos_estado": vehiculos_estado,
        "vehiculos_disponibles_pct": vehiculos_disponibles_pct,
        "vehiculos_en_ruta_pct": vehiculos_en_ruta_pct,
        "vehiculos_mantenimiento_pct": vehiculos_mantenimiento_pct,
        "ultimos_conductores": ultimos_conductores,
        "ultimos_vehiculos": ultimos_vehiculos,
        "ultimos_envios": ultimos_envios,
        "ultimas_alertas": ultimas_alertas,
        "envios_activos": envios_activos,
        "alertas_pendientes": alertas_pendientes,
    }
    return render(request, "dashboard.html", context)


# ✅ Dashboard para Conductores
def dashboard_conductor(request):
    if not request.user.is_authenticated or request.user.rol != 'conductor':
        messages.error(request, "Acceso denegado")
        return redirect('dashboard')
    
    # Envíos del conductor
    envios_conductor = Envio.objects.filter(
        vehiculo__conductor=request.user
    ).select_related('vehiculo', 'cliente')
    
    # Estadísticas
    envios_activos = envios_conductor.filter(estado='en_ruta').count()
    envios_pendientes = envios_conductor.filter(estado='pendiente').count()
    envios_completados = envios_conductor.filter(estado='entregado').count()
    total_envios = envios_conductor.count()
    
    # Envío actual (en ruta)
    envio_actual = envios_conductor.filter(estado='en_ruta').first()
    ultimo_evento = None
    if envio_actual:
        ultimo_evento = EventoEnvio.objects.filter(envio=envio_actual).order_by('-fecha').first()
    
    # Vehículo asignado
    vehiculo = Vehiculo.objects.filter(conductor=request.user).first()
    
    # Últimos envíos
    ultimos_envios = envios_conductor.order_by('-fecha_creacion')[:10]
    
    # Alertas del conductor
    alertas = Alerta.objects.filter(
        envio__vehiculo__conductor=request.user,
        atendida=False
    ).order_by('-fecha')[:5]
    
    context = {
        'envios_activos': envios_activos,
        'envios_pendientes': envios_pendientes,
        'envios_completados': envios_completados,
        'total_envios': total_envios,
        'envio_actual': envio_actual,
        'ultimo_evento': ultimo_evento,
        'vehiculo': vehiculo,
        'ultimos_envios': ultimos_envios,
        'alertas': alertas,
    }
    return render(request, "dashboard_conductor.html", context)


# ✅ Dashboard para Clientes
def dashboard_cliente(request):
    if not request.user.is_authenticated or request.user.rol != 'cliente':
        messages.error(request, "Acceso denegado")
        return redirect('dashboard')
    
    # Envíos del cliente
    envios_cliente = Envio.objects.filter(
        cliente=request.user
    ).select_related('vehiculo', 'vehiculo__conductor')
    
    # Estadísticas
    envios_activos = envios_cliente.filter(estado__in=['pendiente', 'en_ruta']).count()
    envios_completados = envios_cliente.filter(estado='entregado').count()
    envios_con_incidencia = envios_cliente.filter(estado='incidencia').count()
    total_envios = envios_cliente.count()
    
    # Envíos en tránsito
    envios_en_transito = envios_cliente.filter(estado='en_ruta')
    
    # Últimos envíos
    ultimos_envios = envios_cliente.order_by('-fecha_creacion')[:10]
    
    # Alertas de los envíos del cliente
    alertas = Alerta.objects.filter(
        envio__cliente=request.user
    ).order_by('-fecha')[:5]
    
    context = {
        'envios_activos': envios_activos,
        'envios_completados': envios_completados,
        'envios_con_incidencia': envios_con_incidencia,
        'total_envios': total_envios,
        'envios_en_transito': envios_en_transito,
        'ultimos_envios': ultimos_envios,
        'alertas': alertas,
    }
    return render(request, "dashboard_cliente.html", context)


def dashboard_react(request):
    """Dashboard moderno con React Bits"""
    # Reutilizar la misma lógica del dashboard clásico
    # 🔹 Contadores principales
    envios_count = Envio.objects.count()
    vehiculos_count = Vehiculo.objects.count()
    conductores_count = Usuario.objects.filter(rol="conductor").count()
    alertas_count = Alerta.objects.count()

    # 🔹 Envíos por mes (últimos 6 meses)
    envios_por_mes = (
        Envio.objects
        .annotate(mes=TruncMonth("fecha_creacion"))
        .values("mes")
        .annotate(total=Count("id"))
        .order_by("mes")
    )
    meses = [e["mes"].strftime("%b %Y") if e["mes"] else "" for e in envios_por_mes]
    envios_data = [e["total"] for e in envios_por_mes]

    # 🔹 Estado de vehículos
    vehiculos_disponibles = Vehiculo.objects.filter(estado="disponible").count()
    vehiculos_en_ruta = Vehiculo.objects.filter(estado="en_ruta").count()
    vehiculos_mantenimiento = Vehiculo.objects.filter(estado="mantenimiento").count()
    
    vehiculos_data = [vehiculos_disponibles, vehiculos_en_ruta, vehiculos_mantenimiento]
    
    # Calcular porcentajes para la flota
    total_vehiculos = vehiculos_count if vehiculos_count > 0 else 1
    vehiculos_disponibles_pct = round((vehiculos_disponibles / total_vehiculos) * 100)
    vehiculos_en_ruta_pct = round((vehiculos_en_ruta / total_vehiculos) * 100)
    vehiculos_mantenimiento_pct = round((vehiculos_mantenimiento / total_vehiculos) * 100)

    # 🔹 Últimos registros con select_related para optimizar consultas
    ultimos_conductores = Usuario.objects.filter(rol="conductor").order_by("-id")[:5]
    ultimos_vehiculos = Vehiculo.objects.select_related('conductor').order_by("-id")[:5]
    ultimos_envios = Envio.objects.select_related('cliente', 'vehiculo').order_by("-fecha_creacion")[:5]

    context = {
        "envios_count": envios_count,
        "vehiculos_count": vehiculos_count,
        "conductores_count": conductores_count,
        "alertas_count": alertas_count,
        "meses": meses,
        "envios_data": envios_data,
        "vehiculos_data": vehiculos_data,
        "vehiculos_disponibles": vehiculos_disponibles_pct,
        "vehiculos_en_ruta": vehiculos_en_ruta_pct,
        "vehiculos_mantenimiento": vehiculos_mantenimiento_pct,
        "ultimos_conductores": ultimos_conductores,
        "ultimos_vehiculos": ultimos_vehiculos,
        "ultimos_envios": ultimos_envios,
    }
    
    return render(request, "dashboard_react.html", context)

@login_required
def envios_list(request):
    envios = Envio.objects.select_related('cliente', 'vehiculo').all().order_by('-fecha_creacion')
    clientes = Usuario.objects.filter(rol='cliente', activo=True)
    vehiculos = Vehiculo.objects.filter(estado__in=['disponible', 'en_ruta'])
    
    # Estadísticas
    pendientes = Envio.objects.filter(estado='pendiente').count()
    en_ruta = Envio.objects.filter(estado='en_ruta').count()
    entregados = Envio.objects.filter(estado='entregado').count()
    incidencias = Envio.objects.filter(estado='incidencia').count()
    
    context = {
        'envios': envios,
        'clientes': clientes,
        'vehiculos': vehiculos,
        'pendientes': pendientes,
        'en_ruta': en_ruta,
        'entregados': entregados,
        'incidencias': incidencias,
    }
    return render(request, "envios_list.html", context)


@login_required
def vehiculos_list(request):
    vehiculos = Vehiculo.objects.select_related('conductor').all()
    conductores = Usuario.objects.filter(rol='conductor', activo=True)
    
    # Estadísticas
    disponibles = Vehiculo.objects.filter(estado='disponible').count()
    en_ruta = Vehiculo.objects.filter(estado='en_ruta').count()
    mantenimiento = Vehiculo.objects.filter(estado='mantenimiento').count()
    fuera_servicio = Vehiculo.objects.filter(estado='fuera_servicio').count()
    
    context = {
        'vehiculos': vehiculos,
        'conductores': conductores,
        'disponibles': disponibles,
        'en_ruta': en_ruta,
        'mantenimiento': mantenimiento,
        'fuera_servicio': fuera_servicio,
    }
    return render(request, "vehiculos_list.html", context)


@login_required
def alertas_list(request):
    alertas = Alerta.objects.select_related('envio', 'atendida_por').all().order_by("-fecha")
    
    # Estadísticas
    criticas = Alerta.objects.filter(nivel='critica').count()
    altas = Alerta.objects.filter(nivel='alta').count()
    medias = Alerta.objects.filter(nivel='media').count()
    atendidas = Alerta.objects.filter(atendida=True).count()
    
    context = {
        'alertas': alertas,
        'criticas': criticas,
        'altas': altas,
        'medias': medias,
        'atendidas': atendidas,
    }
    return render(request, "alertas_list.html", context)

# ✅ Ver detalle de alerta
def alerta_detalle(request, alerta_id):
    alerta = get_object_or_404(Alerta.objects.select_related('envio', 'envio__vehiculo', 'envio__cliente', 'atendida_por'), pk=alerta_id)
    
    # Obtener eventos relacionados al envío
    eventos = EventoEnvio.objects.filter(envio=alerta.envio).order_by('-fecha')[:10]
    
    context = {
        'alerta': alerta,
        'eventos': eventos,
    }
    return render(request, "alerta_detalle.html", context)

# ✅ Atender alerta
def atender_alerta(request, alerta_id):
    alerta = get_object_or_404(Alerta, pk=alerta_id)
    
    if request.method == "POST":
        alerta.atendida = True
        alerta.atendida_por = request.user
        alerta.fecha_atencion = now()
        alerta.notas_atencion = request.POST.get('notas', '')
        alerta.save()
        
        messages.success(request, f"Alerta {alerta.get_tipo_display()} atendida con éxito ✅")
        return redirect("alertas_list")
    
    return render(request, "alerta_atender.html", {"alerta": alerta})


# ✅ Crear conductor
def crear_conductor(request):
    if request.method == "POST":
        form = ConductorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conductor creado con éxito ✅")
            return redirect("conductores_list")
    else:
        form = ConductorForm()
    return render(request, "conductor_form.html", {"form": form})


# ✅ Listar conductores
@login_required
def conductores_list(request):
    conductores = Usuario.objects.filter(rol="conductor").order_by('-fecha_registro')
    return render(request, "conductores_list.html", {"conductores": conductores})

# ✅ Ver detalle de conductor
def conductor_detalle(request, conductor_id):
    conductor = get_object_or_404(Usuario, id=conductor_id, rol="conductor")
    
    # Obtener vehículo asignado
    try:
        vehiculo = Vehiculo.objects.get(conductor=conductor)
    except Vehiculo.DoesNotExist:
        vehiculo = None
    
    # Obtener envíos del conductor
    envios = Envio.objects.filter(vehiculo__conductor=conductor).order_by('-fecha_creacion')[:10]
    
    # Estadísticas
    total_envios = Envio.objects.filter(vehiculo__conductor=conductor).count()
    envios_completados = Envio.objects.filter(vehiculo__conductor=conductor, estado='entregado').count()
    envios_en_ruta = Envio.objects.filter(vehiculo__conductor=conductor, estado='en_ruta').count()
    
    context = {
        'conductor': conductor,
        'vehiculo': vehiculo,
        'envios': envios,
        'total_envios': total_envios,
        'envios_completados': envios_completados,
        'envios_en_ruta': envios_en_ruta,
    }
    return render(request, "conductor_detalle.html", context)

# ✅ Editar conductor
def editar_conductor(request, conductor_id):
    conductor = get_object_or_404(Usuario, id=conductor_id, rol="conductor")
    
    if request.method == "POST":
        # Actualizar datos
        conductor.first_name = request.POST.get('first_name')
        conductor.last_name = request.POST.get('last_name')
        conductor.email = request.POST.get('email')
        conductor.telefono = request.POST.get('telefono')
        conductor.documento = request.POST.get('documento')
        conductor.activo = request.POST.get('activo') == 'on'
        
        # Cambiar contraseña si se proporciona
        nueva_password = request.POST.get('password')
        if nueva_password:
            conductor.set_password(nueva_password)
        
        conductor.save()
        messages.success(request, f"Conductor {conductor.nombre_completo} actualizado con éxito ✅")
        return redirect("conductor_detalle", conductor_id=conductor.id)
    
    return render(request, "conductor_editar.html", {"conductor": conductor})

# ✅ Panel de rastreo GPS para conductor
@login_required
def conductor_rastreo(request):
    # Verificar que el usuario esté autenticado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta página")
        return redirect("dashboard")
    
    # Verificar que el usuario sea conductor o admin
    if request.user.rol not in ['conductor', 'admin']:
        messages.error(request, "Solo los conductores pueden acceder a esta página")
        return redirect("dashboard")
    
    # Obtener envío activo del conductor (si es conductor)
    envio_activo = None
    if request.user.rol == 'conductor':
        envio_activo = Envio.objects.filter(
            vehiculo__conductor=request.user,
            estado='en_ruta'
        ).first()
    
    context = {
        'envio_activo': envio_activo,
    }
    
    return render(request, "conductor_rastreo.html", context)


# ✅ Crear vehículo
def crear_vehiculo(request):
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo creado con éxito 🚛")
            return redirect("vehiculos_list")
    else:
        form = VehiculoForm()
    return render(request, "vehiculo_form.html", {"form": form})


# ✅ Ver detalle de vehículo
def vehiculo_detalle(request, vehiculo_id):
    vehiculo = Vehiculo.objects.select_related('conductor').get(id=vehiculo_id)
    # Obtener envíos del vehículo
    envios = Envio.objects.filter(vehiculo=vehiculo).order_by('-fecha_creacion')[:10]
    # Obtener envío activo (sin filtrar sobre el slice)
    envio_activo = Envio.objects.filter(vehiculo=vehiculo, estado='en_ruta').first()
    ultimo_evento = None
    if envio_activo:
        ultimo_evento = EventoEnvio.objects.filter(envio=envio_activo).order_by('-fecha').first()
    
    context = {
        'vehiculo': vehiculo,
        'envios': envios,
        'envio_activo': envio_activo,
        'ultimo_evento': ultimo_evento,
    }
    return render(request, "vehiculo_detalle.html", context)


# ✅ Editar vehículo
def editar_vehiculo(request, vehiculo_id):
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    if request.method == "POST":
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado con éxito 🚛")
            return redirect("vehiculo_detalle", vehiculo_id=vehiculo.id)
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, "vehiculo_form.html", {"form": form, "vehiculo": vehiculo})


# ✅ Ver ubicación del vehículo
def vehiculo_ubicacion(request, vehiculo_id):
    vehiculo = Vehiculo.objects.select_related('conductor').get(id=vehiculo_id)
    # Obtener envío activo
    envio_activo = Envio.objects.filter(vehiculo=vehiculo, estado='en_ruta').first()
    
    if not envio_activo:
        messages.warning(request, "Este vehículo no tiene envíos activos")
        return redirect("vehiculo_detalle", vehiculo_id=vehiculo.id)
    
    # Redirigir a la vista de rastreo del envío
    return redirect("rastrear_envio", envio_id=envio_activo.id)


# ✅ Crear envío
def crear_envio(request):
    if request.method == "POST":
        form = EnvioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Envío creado con éxito 📦")
            return redirect("envios_list")
    else:
        form = EnvioForm()
    return render(request, "envio_form.html", {"form": form})


# ✅ Ver detalle de envío
def envio_detalle(request, envio_id):
    envio = Envio.objects.select_related('cliente', 'vehiculo', 'vehiculo__conductor').get(id=envio_id)
    eventos = EventoEnvio.objects.filter(envio=envio).order_by('-fecha')
    alertas = Alerta.objects.filter(envio=envio).order_by('-fecha')
    
    context = {
        'envio': envio,
        'eventos': eventos,
        'alertas': alertas,
    }
    return render(request, "envio_detalle.html", context)


# ✅ Rastrear envío en tiempo real
@login_required
def rastrear_envio(request, envio_id):
    envio = Envio.objects.select_related('cliente', 'vehiculo', 'vehiculo__conductor').get(id=envio_id)
    
    # Obtener todos los eventos GPS del envío
    eventos = EventoEnvio.objects.filter(
        envio=envio,
        latitud__isnull=False,
        longitud__isnull=False
    ).order_by('fecha')
    
    # Último evento
    ultimo_evento = eventos.last()
    
    # Estadísticas
    total_eventos = eventos.count()
    
    # Convertir eventos a JSON para el mapa
    eventos_json = []
    for evento in eventos:
        eventos_json.append({
            'lat': float(evento.latitud),
            'lng': float(evento.longitud),
            'fecha': evento.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'ubicacion': evento.ubicacion or ''
        })
    
    context = {
        'envio': envio,
        'ultimo_evento': ultimo_evento,
        'eventos': eventos,
        'eventos_json': eventos_json,
        'total_eventos': total_eventos,
    }
    return render(request, "envio_rastreo.html", context)


# ✅ Editar envío
def editar_envio(request, envio_id):
    envio = Envio.objects.get(id=envio_id)
    if request.method == "POST":
        form = EnvioForm(request.POST, instance=envio)
        if form.is_valid():
            form.save()
            messages.success(request, "Envío actualizado con éxito ✅")
            return redirect("envio_detalle", envio_id=envio.id)
    else:
        form = EnvioForm(instance=envio)
    return render(request, "envio_form.html", {"form": form, "envio": envio})


@login_required
def panel_rastreo_general(request):
    """Panel para que el admin vea todos los conductores en un mapa."""
    if not request.user.is_staff:
        messages.error(request, "Acceso denegado. Solo para administradores.")
        return redirect("dashboard")

    # Obtener todos los envíos que están actualmente en ruta
    envios_en_ruta = Envio.objects.filter(
        estado='en_ruta'
    ).select_related('vehiculo', 'vehiculo__conductor')

    # Preparar datos para JSON
    envios_json = []
    for envio in envios_en_ruta:
        if envio.vehiculo:
            # Obtener el último evento con ubicación
            ultimo_evento = EventoEnvio.objects.filter(
                envio=envio,
                latitud__isnull=False,
                longitud__isnull=False
            ).order_by('-fecha').first()
            
            if ultimo_evento:
                conductor = envio.vehiculo.conductor
                envios_json.append({
                    'lat': float(ultimo_evento.latitud),
                    'lng': float(ultimo_evento.longitud),
                    'conductor': conductor.nombre_completo if conductor else 'Sin conductor',
                    'vehiculo': envio.vehiculo.placa,
                    'guia': envio.numero_guia,
                    'actualizacion': ultimo_evento.fecha.strftime('%Y-%m-%d %H:%M')
                })

    context = {
        'envios_en_ruta': envios_en_ruta,
        'envios_json': envios_json,
    }
    
    return render(request, "panel_rastreo_general_v2.html", context)


@login_required
def ubicaciones_activas_api(request):
    """API para obtener ubicaciones activas en tiempo real"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Acceso denegado'}, status=403)
    
    envios_en_ruta = Envio.objects.filter(estado='en_ruta').select_related('vehiculo', 'vehiculo__conductor')
    
    ubicaciones = []
    for envio in envios_en_ruta:
        if envio.vehiculo:
            ultimo_evento = EventoEnvio.objects.filter(
                envio=envio,
                latitud__isnull=False,
                longitud__isnull=False
            ).order_by('-fecha').first()
            
            if ultimo_evento:
                conductor = envio.vehiculo.conductor
                
                # Contar actualizaciones del día
                from datetime.datetime import datetime, timedelta
                hoy = datetime.now().date()
                updates_count = EventoEnvio.objects.filter(
                    envio=envio,
                    fecha__date=hoy,
                    latitud__isnull=False
                ).count()
                
                ubicaciones.append({
                    'envio_id': envio.id,
                    'lat': float(ultimo_evento.latitud),
                    'lng': float(ultimo_evento.longitud),
                    'conductor': conductor.nombre_completo if conductor else 'Sin conductor',
                    'vehiculo': envio.vehiculo.placa,
                    'guia': envio.numero_guia,
                    'speed': 0,  # TODO: calcular velocidad real
                    'actualizacion': ultimo_evento.fecha.strftime('%H:%M:%S'),
                    'updates_count': updates_count
                })
    
    return JsonResponse(ubicaciones, safe=False)


# Create your views here.
