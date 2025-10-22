import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from cargas.models import *

print("🇪🇨 Limpiando datos anteriores...")
Sensor.objects.all().delete()
Alerta.objects.all().delete()
EventoEnvio.objects.all().delete()
Envio.objects.all().delete()
Vehiculo.objects.all().delete()
Usuario.objects.filter(is_superuser=False).delete()

print("🇪🇨 Creando usuarios de Ecuador...")

# Admin
admin, _ = Usuario.objects.get_or_create(
    username='admin',
    defaults={'email': 'admin@cargotrack.ec', 'first_name': 'Admin', 'last_name': 'Sistema',
              'rol': 'admin', 'telefono': '+593 99 123 4567', 'documento': '1710123456',
              'is_staff': True, 'is_superuser': True, 'activo': True}
)
admin.set_password('admin123')
admin.save()

# Clientes
clientes = []
for data in [
    ('cliente_quito', 'Carlos', 'Morales', '+593 2 234 5678', '1710234567'),
    ('cliente_guayaquil', 'María', 'Zambrano', '+593 4 345 6789', '0912345678'),
    ('cliente_cuenca', 'Luis', 'Ordóñez', '+593 7 456 7890', '0102345678'),
]:
    u = Usuario.objects.create(username=data[0], first_name=data[1], last_name=data[2],
                               telefono=data[3], documento=data[4], rol='cliente', activo=True,
                               email=f'{data[0]}@empresa.ec')
    u.set_password('cliente123')
    u.save()
    clientes.append(u)

# Conductores
conductores = []
for data in [
    ('conductor1', 'Juan', 'Pérez', '+593 99 234 5678', '1710345678'),
    ('conductor2', 'Pedro', 'García', '+593 98 345 6789', '0912456789'),
    ('conductor3', 'Diego', 'López', '+593 99 456 7890', '0102456789'),
]:
    u = Usuario.objects.create(username=data[0], first_name=data[1], last_name=data[2],
                               telefono=data[3], documento=data[4], rol='conductor', activo=True,
                               email=f'{data[0]}@cargotrack.ec')
    u.set_password('conductor123')
    u.save()
    conductores.append(u)

print(f"✅ {Usuario.objects.count()} usuarios creados")

print("🇪🇨 Creando vehículos...")
vehiculos = []
for data in [
    ('GYE-1234', 'Hino', '500 Series', 2022, 'Blanco', 12.00, conductores[0], 'en_ruta'),
    ('PIC-5678', 'Chevrolet', 'NPR', 2021, 'Azul', 5.00, None, 'disponible'),
    ('AZU-9012', 'Hino', '300 Series', 2023, 'Rojo', 8.00, conductores[1], 'en_ruta'),
    ('TUN-3456', 'Isuzu', 'FTR', 2020, 'Negro', 10.00, None, 'mantenimiento'),
]:
    v = Vehiculo.objects.create(
        placa=data[0], marca=data[1], modelo=data[2], anio=data[3], color=data[4],
        capacidad_toneladas=Decimal(str(data[5])), conductor=data[6], estado=data[7],
        kilometraje=45000
    )
    vehiculos.append(v)

print(f"✅ {Vehiculo.objects.count()} vehículos creados")

print("🇪🇨 Creando envíos...")
envios_data = [
    (clientes[0], vehiculos[0], 'Quito, Pichincha', -0.1807, -78.4678, 'Guayaquil, Guayas', -2.1894, -79.8883, 
     'en_ruta', 'alta', 'Electrodomésticos', 2500, 25000, 4),
    (clientes[1], vehiculos[2], 'Guayaquil, Guayas', -2.1894, -79.8883, 'Cuenca, Azuay', -2.9001, -79.0059,
     'en_ruta', 'urgente', 'Medicamentos', 800, 50000, 3),
    (clientes[2], vehiculos[1], 'Manta, Manabí', -0.9537, -80.7089, 'Quito, Pichincha', -0.1807, -78.4678,
     'pendiente', 'media', 'Productos del mar', 3500, 35000, 0),
]

envios = []
for data in envios_data:
    e = Envio.objects.create(
        cliente=data[0], vehiculo=data[1], origen=data[2], origen_lat=Decimal(str(data[3])),
        origen_lng=Decimal(str(data[4])), destino=data[5], destino_lat=Decimal(str(data[6])),
        destino_lng=Decimal(str(data[7])), estado=data[8], prioridad=data[9],
        descripcion_carga=data[10], peso_kg=Decimal(str(data[11])), valor_declarado=Decimal(str(data[12])),
        contacto_origen='Almacén', telefono_origen='+593 2 300 1234',
        contacto_destino='Tienda', telefono_destino='+593 4 456 7890'
    )
    if data[13] > 0:
        e.fecha_inicio = timezone.now() - timedelta(hours=data[13])
        e.save()
    envios.append(e)

print(f"✅ {Envio.objects.count()} envíos creados")

print("🇪🇨 Creando eventos...")
eventos_data = [
    (envios[0], 'inicio', 'Carga iniciada desde Quito', 'Quito, Av. Simón Bolívar', -0.1807, -78.4678, 4),
    (envios[0], 'checkpoint', 'Peaje Alóag', 'Alóag, Pichincha', -0.5167, -78.6000, 3),
    (envios[1], 'inicio', 'Envío urgente - Medicamentos', 'Guayaquil, Zona Industrial', -2.1894, -79.8883, 3),
    (envios[1], 'checkpoint', 'Vía a Cuenca', 'Naranjal, Guayas', -2.6733, -79.6167, 2),
]

for data in eventos_data:
    EventoEnvio.objects.create(
        envio=data[0], tipo=data[1], descripcion=data[2], ubicacion=data[3],
        latitud=Decimal(str(data[4])), longitud=Decimal(str(data[5])),
        velocidad_kmh=Decimal('70.00'), bateria_dispositivo=95,
        fecha=timezone.now() - timedelta(hours=data[6])
    )

print(f"✅ {EventoEnvio.objects.count()} eventos creados")

print("🇪🇨 Creando alertas...")
Alerta.objects.create(envio=envios[1], tipo='velocidad', nivel='media',
                      descripcion='Velocidad de 85 km/h detectada')
Alerta.objects.create(envio=envios[0], tipo='parada_no_autorizada', nivel='alta',
                      descripcion='Parada no programada - 18 minutos')

print(f"✅ {Alerta.objects.count()} alertas creadas")

print("🇪🇨 Creando sensores...")
Sensor.objects.create(envio=envios[1], tipo='temperatura', valor='6.5', unidad='°C',
                      valor_minimo=Decimal('2.0'), valor_maximo=Decimal('8.0'))
Sensor.objects.create(envio=envios[1], tipo='humedad', valor='62', unidad='%',
                      valor_minimo=Decimal('40.0'), valor_maximo=Decimal('70.0'))
Sensor.objects.create(envio=envios[0], tipo='vibracion', valor='3.2', unidad='g',
                      valor_minimo=Decimal('0.0'), valor_maximo=Decimal('5.0'))

print(f"✅ {Sensor.objects.count()} sensores creados")

print(f"""
{'='*60}
🇪🇨 DATOS DE ECUADOR CREADOS EXITOSAMENTE
{'='*60}

📊 Resumen:
   - Usuarios: {Usuario.objects.count()}
   - Vehículos: {Vehiculo.objects.count()}
   - Envíos: {Envio.objects.count()}
   - Eventos: {EventoEnvio.objects.count()}
   - Alertas: {Alerta.objects.count()}
   - Sensores: {Sensor.objects.count()}

🔐 Credenciales:
   Admin: admin / admin123
   Cliente: cliente_quito / cliente123
   Conductor: conductor1 / conductor123

🌐 Admin: http://127.0.0.1:8000/admin/
""")
