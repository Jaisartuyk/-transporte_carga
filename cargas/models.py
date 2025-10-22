from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class Usuario(AbstractUser):
    """Modelo de usuario extendido con roles para el sistema de trazabilidad"""
    
    ROLES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('conductor', 'Conductor'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente', db_index=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documento = models.CharField(max_length=50, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True, null=True)

    # Solución a los conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',
        blank=True,
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"
    
    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username
    
    def es_conductor(self):
        return self.rol == 'conductor'
    
    def es_cliente(self):
        return self.rol == 'cliente'
    
    def es_admin(self):
        return self.rol == 'admin'


class Vehiculo(models.Model):
    """Modelo de vehículo para la gestión de flota"""
    
    ESTADOS = [
        ("disponible", "Disponible"),
        ("en_ruta", "En ruta"),
        ("mantenimiento", "Mantenimiento"),
        ("fuera_servicio", "Fuera de Servicio"),
    ]
    
    placa = models.CharField(max_length=10, unique=True, db_index=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    capacidad_toneladas = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0.1)]
    )
    conductor = models.OneToOneField(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'rol':'conductor'},
        related_name='vehiculo_asignado'
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible', db_index=True)
    
    # Campos adicionales
    color = models.CharField(max_length=30, blank=True)
    numero_motor = models.CharField(max_length=50, blank=True, null=True)
    numero_chasis = models.CharField(max_length=50, blank=True, null=True)
    kilometraje = models.PositiveIntegerField(default=0)
    ultimo_mantenimiento = models.DateField(blank=True, null=True)
    proximo_mantenimiento = models.DateField(blank=True, null=True)
    foto_vehiculo = models.ImageField(upload_to='vehiculos/', blank=True, null=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['placa']
    
    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"
    
    @property
    def nombre_completo(self):
        return f"{self.marca} {self.modelo} ({self.anio})"
    
    @property
    def esta_disponible(self):
        return self.estado == 'disponible'
    
    @property
    def necesita_mantenimiento(self):
        if self.proximo_mantenimiento:
            return self.proximo_mantenimiento <= timezone.now().date()
        return False
    
    def asignar_conductor(self, conductor):
        if conductor.es_conductor():
            self.conductor = conductor
            self.save()
            return True
        return False


class Envio(models.Model):
    """Modelo de envío para trazabilidad de carga"""
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En Ruta'),
        ('entregado', 'Entregado'),
        ('incidencia', 'Con Incidencia'),
        ('cancelado', 'Cancelado'),
    ]
    
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    # Generar número de guía automáticamente
    numero_guia = models.CharField(
        max_length=50, 
        unique=True, 
        db_index=True,
        blank=True
    )
    
    cliente = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name="envios", 
        limit_choices_to={'rol':'cliente'}
    )
    vehiculo = models.ForeignKey(
        Vehiculo, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='envios'
    )
    
    # Información de origen y destino
    origen = models.CharField(max_length=150)
    origen_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    origen_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    destino = models.CharField(max_length=150)
    destino_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    destino_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    fecha_estimada_entrega = models.DateTimeField(blank=True, null=True)
    
    # Estado y prioridad
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', db_index=True)
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='media', blank=True)
    
    # Información de carga
    descripcion_carga = models.TextField(blank=True)
    peso_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_declarado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Contactos
    contacto_origen = models.CharField(max_length=100, blank=True)
    telefono_origen = models.CharField(max_length=20, blank=True)
    contacto_destino = models.CharField(max_length=100, blank=True)
    telefono_destino = models.CharField(max_length=20, blank=True)
    
    # Notas y observaciones
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Envío'
        verbose_name_plural = 'Envíos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['numero_guia']),
            models.Index(fields=['estado', 'fecha_creacion']),
        ]

    def save(self, *args, **kwargs):
        if not self.numero_guia:
            # Generar número de guía único
            self.numero_guia = f"ENV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Envío {self.numero_guia} - {self.get_estado_display()}"
    
    @property
    def esta_en_transito(self):
        return self.estado == 'en_ruta'
    
    @property
    def fue_entregado(self):
        return self.estado == 'entregado'
    
    @property
    def tiene_incidencias(self):
        return self.estado == 'incidencia'
    
    @property
    def duracion_transporte(self):
        if self.fecha_inicio and self.fecha_entrega:
            return self.fecha_entrega - self.fecha_inicio
        return None
    
    @property
    def conductor_asignado(self):
        if self.vehiculo and self.vehiculo.conductor:
            return self.vehiculo.conductor
        return None
    
    def iniciar_envio(self):
        self.estado = 'en_ruta'
        self.fecha_inicio = timezone.now()
        self.save()
    
    def completar_envio(self):
        self.estado = 'entregado'
        self.fecha_entrega = timezone.now()
        self.save()
    
    def reportar_incidencia(self, descripcion):
        self.estado = 'incidencia'
        self.save()
        # Crear alerta automáticamente
        Alerta.objects.create(
            envio=self,
            tipo='otro',
            descripcion=descripcion
        )


class EventoEnvio(models.Model):
    """Modelo para registro de eventos y tracking GPS"""
    
    TIPOS_EVENTO = [
        ('inicio', 'Inicio de Ruta'),
        ('checkpoint', 'Punto de Control'),
        ('parada', 'Parada'),
        ('incidente', 'Incidente'),
        ('entrega', 'Entrega'),
    ]
    
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="eventos")
    tipo = models.CharField(max_length=20, choices=TIPOS_EVENTO, default='checkpoint')
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    fecha = models.DateTimeField(default=now)
    
    # Campos adicionales
    foto_evidencia = models.ImageField(upload_to='eventos/', blank=True, null=True)
    velocidad_kmh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bateria_dispositivo = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Evento de Envío'
        verbose_name_plural = 'Eventos de Envío'
        ordering = ['-fecha']

    def __str__(self):
        return f"Evento {self.get_tipo_display()} - {self.envio.numero_guia} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def tiene_ubicacion(self):
        return self.latitud is not None and self.longitud is not None


class Alerta(models.Model):
    """Modelo para sistema de alertas y seguridad"""
    
    TIPOS = [
        ('robo', 'Robo'),
        ('accidente', 'Accidente'),
        ('desvio', 'Desvío de ruta'),
        ('velocidad', 'Exceso de Velocidad'),
        ('parada_no_autorizada', 'Parada No Autorizada'),
        ('perdida_señal', 'Pérdida de Señal GPS'),
        ('otro', 'Otro'),
    ]
    
    NIVELES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="alertas")
    tipo = models.CharField(max_length=30, choices=TIPOS)
    nivel = models.CharField(max_length=20, choices=NIVELES, default='media')
    descripcion = models.TextField()
    fecha = models.DateTimeField(default=now)
    atendida = models.BooleanField(default=False)
    fecha_atencion = models.DateTimeField(blank=True, null=True)
    atendida_por = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alertas_atendidas'
    )
    notas_atencion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha']

    def __str__(self):
        return f"Alerta {self.get_tipo_display()} - {self.envio.numero_guia}"
    
    def atender(self, usuario, notas=''):
        self.atendida = True
        self.fecha_atencion = timezone.now()
        self.atendida_por = usuario
        self.notas_atencion = notas
        self.save()
    
    @property
    def es_critica(self):
        return self.nivel == 'critica'


class Sensor(models.Model):
    """Modelo para datos de sensores IoT"""
    
    TIPOS_SENSOR = [
        ('temperatura', 'Temperatura'),
        ('humedad', 'Humedad'),
        ('vibracion', 'Vibración'),
        ('presion', 'Presión'),
        ('luz', 'Luz'),
        ('apertura', 'Apertura de Puerta'),
    ]
    
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="sensores")
    tipo = models.CharField(max_length=50, choices=TIPOS_SENSOR)
    valor = models.CharField(max_length=50)
    unidad = models.CharField(max_length=20, blank=True)
    fecha = models.DateTimeField(default=now)
    
    # Umbrales para alertas
    valor_minimo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_maximo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Sensor'
        verbose_name_plural = 'Sensores'
        ordering = ['-fecha']

    def __str__(self):
        return f"Sensor {self.get_tipo_display()} - {self.valor} {self.unidad}"
    
    @property
    def fuera_de_rango(self):
        try:
            valor_num = float(self.valor)
            if self.valor_minimo and valor_num < float(self.valor_minimo):
                return True
            if self.valor_maximo and valor_num > float(self.valor_maximo):
                return True
        except ValueError:
            pass
        return False
