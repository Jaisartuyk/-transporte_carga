from rest_framework import serializers
from .models import Usuario, Vehiculo, Envio, EventoEnvio, Alerta, Sensor


# ============================================================================
# USUARIO SERIALIZER
# ============================================================================
class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    
    nombre_completo = serializers.CharField(read_only=True)
    es_conductor = serializers.BooleanField(read_only=True)
    es_cliente = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'rol', 'telefono', 'documento', 'foto_perfil',
            'activo', 'fecha_registro', 'nombre_completo',
            'es_conductor', 'es_cliente'
        ]
        read_only_fields = ['fecha_registro', 'ultima_actualizacion']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class UsuarioSimpleSerializer(serializers.ModelSerializer):
    """Serializer simplificado para referencias anidadas"""
    
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre_completo', 'telefono', 'rol']


# ============================================================================
# VEHÍCULO SERIALIZER
# ============================================================================
class VehiculoSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Vehículo"""
    
    conductor_info = UsuarioSimpleSerializer(source='conductor', read_only=True)
    esta_disponible = serializers.BooleanField(read_only=True)
    necesita_mantenimiento = serializers.BooleanField(read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    
    class Meta:
        model = Vehiculo
        fields = [
            'id', 'placa', 'marca', 'modelo', 'anio', 'color',
            'capacidad_toneladas', 'numero_motor', 'numero_chasis',
            'kilometraje', 'conductor', 'conductor_info', 'estado',
            'ultimo_mantenimiento', 'proximo_mantenimiento',
            'foto_vehiculo', 'fecha_registro', 'esta_disponible',
            'necesita_mantenimiento', 'nombre_completo'
        ]
        read_only_fields = ['fecha_registro', 'ultima_actualizacion']


class VehiculoSimpleSerializer(serializers.ModelSerializer):
    """Serializer simplificado para referencias anidadas"""
    
    conductor_nombre = serializers.CharField(source='conductor.nombre_completo', read_only=True)
    
    class Meta:
        model = Vehiculo
        fields = ['id', 'placa', 'marca', 'modelo', 'estado', 'conductor_nombre']


# ============================================================================
# EVENTO ENVÍO SERIALIZER
# ============================================================================
class EventoEnvioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo EventoEnvio"""
    
    tiene_ubicacion = serializers.BooleanField(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = EventoEnvio
        fields = [
            'id', 'envio', 'tipo', 'tipo_display', 'descripcion',
            'ubicacion', 'latitud', 'longitud', 'fecha',
            'foto_evidencia', 'velocidad_kmh', 'bateria_dispositivo',
            'tiene_ubicacion'
        ]
        read_only_fields = ['fecha']


class EventoEnvioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear eventos desde app móvil"""
    
    class Meta:
        model = EventoEnvio
        fields = [
            'envio', 'tipo', 'descripcion', 'ubicacion',
            'latitud', 'longitud', 'foto_evidencia',
            'velocidad_kmh', 'bateria_dispositivo'
        ]


# ============================================================================
# ALERTA SERIALIZER
# ============================================================================
class AlertaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Alerta"""
    
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    atendida_por_info = UsuarioSimpleSerializer(source='atendida_por', read_only=True)
    es_critica = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Alerta
        fields = [
            'id', 'envio', 'tipo', 'tipo_display', 'nivel', 'nivel_display',
            'descripcion', 'fecha', 'atendida', 'fecha_atencion',
            'atendida_por', 'atendida_por_info', 'notas_atencion',
            'es_critica'
        ]
        read_only_fields = ['fecha', 'fecha_atencion']


class AlertaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear alertas desde app móvil"""
    
    class Meta:
        model = Alerta
        fields = ['envio', 'tipo', 'nivel', 'descripcion']


# ============================================================================
# SENSOR SERIALIZER
# ============================================================================
class SensorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Sensor"""
    
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    fuera_de_rango = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Sensor
        fields = [
            'id', 'envio', 'tipo', 'tipo_display', 'valor', 'unidad',
            'valor_minimo', 'valor_maximo', 'fecha', 'fuera_de_rango'
        ]
        read_only_fields = ['fecha']


# ============================================================================
# ENVÍO SERIALIZER
# ============================================================================
class EnvioSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Envío"""
    
    cliente_info = UsuarioSimpleSerializer(source='cliente', read_only=True)
    vehiculo_info = VehiculoSimpleSerializer(source='vehiculo', read_only=True)
    conductor_asignado = UsuarioSimpleSerializer(read_only=True)
    
    # Eventos, alertas y sensores anidados
    eventos = EventoEnvioSerializer(many=True, read_only=True)
    alertas = AlertaSerializer(many=True, read_only=True)
    sensores = SensorSerializer(many=True, read_only=True)
    
    # Properties del modelo
    esta_en_transito = serializers.BooleanField(read_only=True)
    fue_entregado = serializers.BooleanField(read_only=True)
    tiene_incidencias = serializers.BooleanField(read_only=True)
    duracion_transporte = serializers.SerializerMethodField()
    
    # Display fields
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    prioridad_display = serializers.CharField(source='get_prioridad_display', read_only=True)

    class Meta:
        model = Envio
        fields = [
            'id', 'numero_guia', 'cliente', 'cliente_info', 'vehiculo', 'vehiculo_info',
            'conductor_asignado', 'origen', 'origen_lat', 'origen_lng',
            'destino', 'destino_lat', 'destino_lng', 'fecha_creacion',
            'fecha_inicio', 'fecha_entrega', 'fecha_estimada_entrega',
            'estado', 'estado_display', 'prioridad', 'prioridad_display',
            'descripcion_carga', 'peso_kg', 'valor_declarado',
            'contacto_origen', 'telefono_origen', 'contacto_destino', 'telefono_destino',
            'notas', 'eventos', 'alertas', 'sensores',
            'esta_en_transito', 'fue_entregado', 'tiene_incidencias', 'duracion_transporte'
        ]
        read_only_fields = ['numero_guia', 'fecha_creacion']
    
    def get_duracion_transporte(self, obj):
        """Retorna la duración del transporte en formato legible"""
        if obj.duracion_transporte:
            return str(obj.duracion_transporte)
        return None


class EnvioSimpleSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listados"""
    
    cliente_nombre = serializers.CharField(source='cliente.nombre_completo', read_only=True)
    conductor_nombre = serializers.CharField(source='conductor_asignado.nombre_completo', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    prioridad_display = serializers.CharField(source='get_prioridad_display', read_only=True)
    
    class Meta:
        model = Envio
        fields = [
            'id', 'numero_guia', 'cliente_nombre', 'conductor_nombre',
            'origen', 'destino', 'estado', 'estado_display',
            'prioridad', 'prioridad_display', 'fecha_creacion'
        ]


class EnvioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear envíos"""
    
    class Meta:
        model = Envio
        fields = [
            'cliente', 'vehiculo', 'origen', 'origen_lat', 'origen_lng',
            'destino', 'destino_lat', 'destino_lng', 'prioridad',
            'descripcion_carga', 'peso_kg', 'valor_declarado',
            'contacto_origen', 'telefono_origen', 'contacto_destino',
            'telefono_destino', 'fecha_estimada_entrega', 'notas'
        ]


# ============================================================================
# SERIALIZERS PARA ACCIONES ESPECÍFICAS
# ============================================================================
class IniciarEnvioSerializer(serializers.Serializer):
    """Serializer para iniciar un envío"""
    envio_id = serializers.IntegerField()


class CompletarEnvioSerializer(serializers.Serializer):
    """Serializer para completar un envío"""
    envio_id = serializers.IntegerField()
    notas = serializers.CharField(required=False, allow_blank=True)


class ReportarIncidenciaSerializer(serializers.Serializer):
    """Serializer para reportar una incidencia"""
    envio_id = serializers.IntegerField()
    descripcion = serializers.CharField()
    tipo_alerta = serializers.ChoiceField(choices=Alerta.TIPOS, default='otro')
    nivel = serializers.ChoiceField(choices=Alerta.NIVELES, default='media')
