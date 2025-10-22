from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('conductor', 'Conductor'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documento = models.CharField(max_length=50, blank=True, null=True)

    # 🔹 Solución a los conflictos
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

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
class Vehiculo(models.Model):
    ESTADOS = [
        ("disponible", "Disponible"),
        ("en_ruta", "En ruta"),
        ("mantenimiento", "Mantenimiento"),
    ]
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.PositiveIntegerField()
    capacidad_toneladas = models.DecimalField(max_digits=6, decimal_places=2)
    conductor = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol':'conductor'})
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

class Envio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_ruta', 'En Ruta'),
        ('entregado', 'Entregado'),
        ('incidencia', 'Con Incidencia'),
    ]

    numero_guia = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="envios", limit_choices_to={'rol':'cliente'})
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    origen = models.CharField(max_length=150)
    destino = models.CharField(max_length=150)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Envío {self.numero_guia} - {self.estado}"



class EventoEnvio(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="eventos")
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=150, blank=True, null=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    fecha = models.DateTimeField(default=now)

    def __str__(self):
        return f"Evento {self.envio.numero_guia} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"

class Alerta(models.Model):
    TIPOS = [
        ('robo', 'Robo'),
        ('accidente', 'Accidente'),
        ('desvio', 'Desvío de ruta'),
        ('otro', 'Otro'),
    ]

    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="alertas")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    fecha = models.DateTimeField(default=now)
    atendida = models.BooleanField(default=False)

    def __str__(self):
        return f"Alerta {self.tipo} - {self.envio.numero_guia}"
    
class Sensor(models.Model):
    envio = models.ForeignKey(Envio, on_delete=models.CASCADE, related_name="sensores")
    tipo = models.CharField(max_length=50)  # ej. temperatura, vibración
    valor = models.CharField(max_length=50)
    fecha = models.DateTimeField(default=now)

    def __str__(self):
        return f"Sensor {self.tipo} - {self.valor}"

# Create your models here.
