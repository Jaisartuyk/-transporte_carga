from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import Usuario, Vehiculo, Envio, EventoEnvio, Alerta, Sensor


# ============================================================================
# USUARIO ADMIN
# ============================================================================
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin personalizado para el modelo Usuario"""
    
    list_display = ['username', 'email', 'rol', 'nombre_completo', 'activo', 'fecha_registro']
    list_filter = ['rol', 'activo', 'is_staff', 'is_superuser', 'fecha_registro']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'documento', 'telefono']
    ordering = ['-fecha_registro']
    
    fieldsets = (
        ('Información de Cuenta', {
            'fields': ('username', 'password', 'email')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'documento', 'telefono', 'foto_perfil')
        }),
        ('Rol y Permisos', {
            'fields': ('rol', 'is_active', 'activo', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined', 'fecha_registro', 'ultima_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_registro', 'ultima_actualizacion', 'last_login', 'date_joined']
    
    def nombre_completo(self, obj):
        return obj.nombre_completo
    nombre_completo.short_description = 'Nombre Completo'


# ============================================================================
# VEHÍCULO ADMIN
# ============================================================================
@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    """Admin personalizado para el modelo Vehículo"""
    
    list_display = ['placa', 'marca_modelo', 'anio', 'estado_badge', 'conductor_asignado', 
                    'capacidad_toneladas', 'necesita_mantenimiento_badge']
    list_filter = ['estado', 'marca', 'anio', 'fecha_registro']
    search_fields = ['placa', 'marca', 'modelo', 'numero_motor', 'numero_chasis']
    ordering = ['placa']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('placa', 'marca', 'modelo', 'anio', 'color', 'capacidad_toneladas')
        }),
        ('Información Técnica', {
            'fields': ('numero_motor', 'numero_chasis', 'kilometraje')
        }),
        ('Estado y Conductor', {
            'fields': ('estado', 'conductor')
        }),
        ('Mantenimiento', {
            'fields': ('ultimo_mantenimiento', 'proximo_mantenimiento')
        }),
        ('Multimedia', {
            'fields': ('foto_vehiculo',)
        }),
        ('Fechas', {
            'fields': ('fecha_registro', 'ultima_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['fecha_registro', 'ultima_actualizacion']
    
    def marca_modelo(self, obj):
        return f"{obj.marca} {obj.modelo}"
    marca_modelo.short_description = 'Vehículo'
    
    def estado_badge(self, obj):
        colors = {
            'disponible': 'green',
            'en_ruta': 'orange',
            'mantenimiento': 'red',
            'fuera_servicio': 'gray'
        }
        color = colors.get(obj.estado, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def conductor_asignado(self, obj):
        if obj.conductor:
            return obj.conductor.nombre_completo
        return format_html('<span style="color: gray;">Sin asignar</span>')
    conductor_asignado.short_description = 'Conductor'
    
    def necesita_mantenimiento_badge(self, obj):
        if obj.necesita_mantenimiento:
            return format_html('<span style="color: red;">⚠️ Sí</span>')
        return format_html('<span style="color: green;">✓ No</span>')
    necesita_mantenimiento_badge.short_description = 'Necesita Mantenimiento'


# ============================================================================
# ENVÍO ADMIN
# ============================================================================
@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    """Admin personalizado para el modelo Envío"""
    
    list_display = ['numero_guia', 'cliente', 'estado_badge', 'prioridad_badge', 
                    'origen', 'destino', 'conductor_info', 'fecha_creacion']
    list_filter = ['estado', 'prioridad', 'fecha_creacion', 'fecha_entrega']
    search_fields = ['numero_guia', 'origen', 'destino', 'descripcion_carga', 
                     'cliente__username', 'cliente__email']
    ordering = ['-fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_guia', 'cliente', 'vehiculo', 'estado', 'prioridad')
        }),
        ('Origen', {
            'fields': ('origen', 'origen_lat', 'origen_lng', 'contacto_origen', 'telefono_origen')
        }),
        ('Destino', {
            'fields': ('destino', 'destino_lat', 'destino_lng', 'contacto_destino', 'telefono_destino')
        }),
        ('Información de Carga', {
            'fields': ('descripcion_carga', 'peso_kg', 'valor_declarado')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_inicio', 'fecha_estimada_entrega', 'fecha_entrega')
        }),
        ('Notas y Observaciones', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['numero_guia', 'fecha_creacion']
    
    actions = ['iniciar_envios', 'completar_envios', 'marcar_como_incidencia']
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': '#fbbf24',
            'en_ruta': '#3b82f6',
            'entregado': '#10b981',
            'incidencia': '#ef4444',
            'cancelado': '#6b7280'
        }
        color = colors.get(obj.estado, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def prioridad_badge(self, obj):
        colors = {
            'baja': '#10b981',
            'media': '#fbbf24',
            'alta': '#f59e0b',
            'urgente': '#ef4444'
        }
        color = colors.get(obj.prioridad, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_prioridad_display()
        )
    prioridad_badge.short_description = 'Prioridad'
    
    def conductor_info(self, obj):
        conductor = obj.conductor_asignado
        if conductor:
            return format_html(
                '<span title="{}">👤 {}</span>',
                conductor.telefono or 'Sin teléfono',
                conductor.nombre_completo
            )
        return format_html('<span style="color: gray;">Sin asignar</span>')
    conductor_info.short_description = 'Conductor'
    
    # Acciones personalizadas
    def iniciar_envios(self, request, queryset):
        count = 0
        for envio in queryset:
            if envio.estado == 'pendiente':
                envio.iniciar_envio()
                count += 1
        self.message_user(request, f'{count} envío(s) iniciado(s) exitosamente.')
    iniciar_envios.short_description = 'Iniciar envíos seleccionados'
    
    def completar_envios(self, request, queryset):
        count = 0
        for envio in queryset:
            if envio.estado == 'en_ruta':
                envio.completar_envio()
                count += 1
        self.message_user(request, f'{count} envío(s) completado(s) exitosamente.')
    completar_envios.short_description = 'Completar envíos seleccionados'
    
    def marcar_como_incidencia(self, request, queryset):
        count = queryset.update(estado='incidencia')
        self.message_user(request, f'{count} envío(s) marcado(s) con incidencia.')
    marcar_como_incidencia.short_description = 'Marcar como incidencia'


# ============================================================================
# EVENTO ENVÍO ADMIN
# ============================================================================
@admin.register(EventoEnvio)
class EventoEnvioAdmin(admin.ModelAdmin):
    """Admin personalizado para el modelo EventoEnvio"""
    
    list_display = ['envio', 'tipo_badge', 'descripcion_corta', 'ubicacion', 
                    'tiene_gps', 'velocidad_kmh', 'fecha']
    list_filter = ['tipo', 'fecha', 'envio__estado']
    search_fields = ['envio__numero_guia', 'descripcion', 'ubicacion']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Evento', {
            'fields': ('envio', 'tipo', 'descripcion')
        }),
        ('Ubicación', {
            'fields': ('ubicacion', 'latitud', 'longitud')
        }),
        ('Datos Adicionales', {
            'fields': ('velocidad_kmh', 'bateria_dispositivo', 'foto_evidencia')
        }),
        ('Fecha', {
            'fields': ('fecha',)
        }),
    )
    
    readonly_fields = ['fecha']
    
    def tipo_badge(self, obj):
        colors = {
            'inicio': '#3b82f6',
            'checkpoint': '#10b981',
            'parada': '#fbbf24',
            'incidente': '#ef4444',
            'entrega': '#8b5cf6'
        }
        color = colors.get(obj.tipo, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_tipo_display()
        )
    tipo_badge.short_description = 'Tipo'
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'
    
    def tiene_gps(self, obj):
        if obj.tiene_ubicacion:
            return format_html('<span style="color: green;">✓ Sí</span>')
        return format_html('<span style="color: red;">✗ No</span>')
    tiene_gps.short_description = 'GPS'


# ============================================================================
# ALERTA ADMIN
# ============================================================================
@admin.register(Alerta)
class AlertaAdmin(admin.ModelAdmin):
    """Admin personalizado para el modelo Alerta"""
    
    list_display = ['envio', 'tipo_badge', 'nivel_badge', 'descripcion_corta', 
                    'atendida_badge', 'fecha']
    list_filter = ['tipo', 'nivel', 'atendida', 'fecha']
    search_fields = ['envio__numero_guia', 'descripcion', 'notas_atencion']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de la Alerta', {
            'fields': ('envio', 'tipo', 'nivel', 'descripcion')
        }),
        ('Estado de Atención', {
            'fields': ('atendida', 'fecha_atencion', 'atendida_por', 'notas_atencion')
        }),
        ('Fecha', {
            'fields': ('fecha',)
        }),
    )
    
    readonly_fields = ['fecha']
    
    actions = ['marcar_como_atendida']
    
    def tipo_badge(self, obj):
        colors = {
            'robo': '#dc2626',
            'accidente': '#ea580c',
            'desvio': '#f59e0b',
            'velocidad': '#fbbf24',
            'parada_no_autorizada': '#f97316',
            'perdida_señal': '#6b7280',
            'otro': '#9ca3af'
        }
        color = colors.get(obj.tipo, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_tipo_display()
        )
    tipo_badge.short_description = 'Tipo'
    
    def nivel_badge(self, obj):
        colors = {
            'baja': '#10b981',
            'media': '#fbbf24',
            'alta': '#f59e0b',
            'critica': '#ef4444'
        }
        icons = {
            'baja': 'ℹ️',
            'media': '⚠️',
            'alta': '🔶',
            'critica': '🚨'
        }
        color = colors.get(obj.nivel, '#6b7280')
        icon = icons.get(obj.nivel, '•')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{} {}</span>',
            color, icon, obj.get_nivel_display()
        )
    nivel_badge.short_description = 'Nivel'
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'
    
    def atendida_badge(self, obj):
        if obj.atendida:
            return format_html('<span style="color: green; font-weight: bold;">✓ Atendida</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Pendiente</span>')
    atendida_badge.short_description = 'Estado'
    
    # Acción personalizada
    def marcar_como_atendida(self, request, queryset):
        count = 0
        for alerta in queryset:
            if not alerta.atendida:
                alerta.atender(usuario=request.user, notas='Atendida desde admin')
                count += 1
        self.message_user(request, f'{count} alerta(s) marcada(s) como atendida(s).')
    marcar_como_atendida.short_description = 'Marcar como atendida'


# ============================================================================
# SENSOR ADMIN
# ============================================================================
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    """Admin personalizado para el modelo Sensor"""
    
    list_display = ['envio', 'tipo_badge', 'valor_display', 'fuera_rango_badge', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['envio__numero_guia', 'tipo', 'valor']
    ordering = ['-fecha']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Sensor', {
            'fields': ('envio', 'tipo', 'valor', 'unidad')
        }),
        ('Umbrales', {
            'fields': ('valor_minimo', 'valor_maximo')
        }),
        ('Fecha', {
            'fields': ('fecha',)
        }),
    )
    
    readonly_fields = ['fecha']
    
    def tipo_badge(self, obj):
        colors = {
            'temperatura': '#ef4444',
            'humedad': '#3b82f6',
            'vibracion': '#f59e0b',
            'presion': '#8b5cf6',
            'luz': '#fbbf24',
            'apertura': '#10b981'
        }
        color = colors.get(obj.tipo, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_tipo_display()
        )
    tipo_badge.short_description = 'Tipo'
    
    def valor_display(self, obj):
        return f"{obj.valor} {obj.unidad}" if obj.unidad else obj.valor
    valor_display.short_description = 'Valor'
    
    def fuera_rango_badge(self, obj):
        if obj.fuera_de_rango:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ Fuera de rango</span>')
        return format_html('<span style="color: green;">✓ Normal</span>')
    fuera_rango_badge.short_description = 'Estado'


# Personalizar el sitio admin
admin.site.site_header = "CargoTrack Pro - Administración"
admin.site.site_title = "CargoTrack Pro"
admin.site.index_title = "Panel de Control de Trazabilidad"

