#!/usr/bin/env python
"""
Script para crear datos de prueba para el sistema de trazabilidad
Ejecutar: python crear_datos_prueba.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from cargas.models import Usuario, Vehiculo, Envio, EventoEnvio, Alerta, Sensor


def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def crear_usuarios():
    print_header("Creando Usuarios")
    
    # Admin
    admin, created = Usuario.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@cargotrack.com',
            'first_name': 'Admin',
            'last_name': 'Sistema',
            'rol': 'admin',
            'telefono': '+57 300 1234567',
            'documento': '1000000001',
            'is_staff': True,
            'is_superuser': True,
            'activo': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"✅ Admin creado: {admin.username}")
    else:
        print(f"ℹ️  Admin ya existe: {admin.username}")
    
    # Clientes
    clientes_data = [
        {
            'username': 'cliente1',
            'email': 'cliente1@empresa.com',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez',
            'telefono': '+57 300 2345678',
            'documento': '1000000002'
        },
        {
            'username': 'cliente2',
            'email': 'cliente2@empresa.com',
            'first_name': 'María',
            'last_name': 'González',
            'telefono': '+57 300 3456789',
            'documento': '1000000003'
        },
        {
            'username': 'cliente3',
            'email': 'cliente3@empresa.com',
            'first_name': 'Luis',
            'last_name': 'Martínez',
            'telefono': '+57 300 4567890',
            'documento': '1000000004'
        }
    ]
    
    clientes = []
    for data in clientes_data:
        cliente, created = Usuario.objects.get_or_create(
            username=data['username'],
            defaults={**data, 'rol': 'cliente', 'activo': True}
        )
        if created:
            cliente.set_password('cliente123')
            cliente.save()
            print(f"✅ Cliente creado: {cliente.nombre_completo}")
        else:
            print(f"ℹ️  Cliente ya existe: {cliente.nombre_completo}")
        clientes.append(cliente)
    
    # Conductores
    conductores_data = [
        {
            'username': 'conductor1',
            'email': 'conductor1@cargotrack.com',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'telefono': '+57 310 1234567',
            'documento': '1000000005'
        },
        {
            'username': 'conductor2',
            'email': 'conductor2@cargotrack.com',
            'first_name': 'Pedro',
            'last_name': 'Sánchez',
            'telefono': '+57 310 2345678',
            'documento': '1000000006'
        },
        {
            'username': 'conductor3',
            'email': 'conductor3@cargotrack.com',
            'first_name': 'Diego',
            'last_name': 'López',
            'telefono': '+57 310 3456789',
            'documento': '1000000007'
        },
        {
            'username': 'conductor4',
            'email': 'conductor4@cargotrack.com',
            'first_name': 'Andrés',
            'last_name': 'Torres',
            'telefono': '+57 310 4567890',
            'documento': '1000000008'
        }
    ]
    
    conductores = []
    for data in conductores_data:
        conductor, created = Usuario.objects.get_or_create(
            username=data['username'],
            defaults={**data, 'rol': 'conductor', 'activo': True}
        )
        if created:
            conductor.set_password('conductor123')
            conductor.save()
            print(f"✅ Conductor creado: {conductor.nombre_completo}")
        else:
            print(f"ℹ️  Conductor ya existe: {conductor.nombre_completo}")
        conductores.append(conductor)
    
    return admin, clientes, conductores


def crear_vehiculos(conductores):
    print_header("Creando Vehículos")
    
    vehiculos_data = [
        {
            'placa': 'ABC123',
            'marca': 'Volvo',
            'modelo': 'FH16',
            'anio': 2022,
            'color': 'Blanco',
            'capacidad_toneladas': Decimal('30.00'),
            'numero_motor': 'VOL123456',
            'numero_chasis': 'CHASIS123456',
            'kilometraje': 45000,
            'estado': 'en_ruta',
            'conductor': conductores[0] if len(conductores) > 0 else None
        },
        {
            'placa': 'DEF456',
            'marca': 'Mercedes-Benz',
            'modelo': 'Actros',
            'anio': 2021,
            'color': 'Azul',
            'capacidad_toneladas': Decimal('25.00'),
            'numero_motor': 'MB789012',
            'numero_chasis': 'CHASIS789012',
            'kilometraje': 62000,
            'estado': 'disponible',
            'conductor': None
        },
        {
            'placa': 'GHI789',
            'marca': 'Scania',
            'modelo': 'R450',
            'anio': 2023,
            'color': 'Rojo',
            'capacidad_toneladas': Decimal('28.00'),
            'numero_motor': 'SCA345678',
            'numero_chasis': 'CHASIS345678',
            'kilometraje': 15000,
            'estado': 'en_ruta',
            'conductor': conductores[1] if len(conductores) > 1 else None
        },
        {
            'placa': 'JKL012',
            'marca': 'Kenworth',
            'modelo': 'T680',
            'anio': 2020,
            'color': 'Negro',
            'capacidad_toneladas': Decimal('32.00'),
            'numero_motor': 'KEN901234',
            'numero_chasis': 'CHASIS901234',
            'kilometraje': 95000,
            'estado': 'mantenimiento',
            'conductor': None,
            'proximo_mantenimiento': timezone.now().date() - timedelta(days=5)
        },
        {
            'placa': 'MNO345',
            'marca': 'Freightliner',
            'modelo': 'Cascadia',
            'anio': 2022,
            'color': 'Gris',
            'capacidad_toneladas': Decimal('27.00'),
            'numero_motor': 'FRE567890',
            'numero_chasis': 'CHASIS567890',
            'kilometraje': 38000,
            'estado': 'disponible',
            'conductor': None
        }
    ]
    
    vehiculos = []
    for data in vehiculos_data:
        vehiculo, created = Vehiculo.objects.get_or_create(
            placa=data['placa'],
            defaults=data
        )
        if created:
            print(f"✅ Vehículo creado: {vehiculo.placa} - {vehiculo.marca} {vehiculo.modelo}")
        else:
            print(f"ℹ️  Vehículo ya existe: {vehiculo.placa}")
        vehiculos.append(vehiculo)
    
    return vehiculos


def crear_envios(clientes, vehiculos):
    print_header("Creando Envíos")
    
    envios_data = [
        {
            'cliente': clientes[0] if len(clientes) > 0 else None,
            'vehiculo': vehiculos[0] if len(vehiculos) > 0 else None,
            'origen': 'Bogotá, Colombia',
            'origen_lat': Decimal('4.7110'),
            'origen_lng': Decimal('-74.0721'),
            'destino': 'Medellín, Colombia',
            'destino_lat': Decimal('6.2476'),
            'destino_lng': Decimal('-75.5658'),
            'estado': 'en_ruta',
            'prioridad': 'alta',
            'descripcion_carga': 'Electrodomésticos - Refrigeradores y lavadoras',
            'peso_kg': Decimal('2500.00'),
            'valor_declarado': Decimal('50000000.00'),
            'contacto_origen': 'Almacén Central',
            'telefono_origen': '+57 1 3001234',
            'contacto_destino': 'Tienda Medellín',
            'telefono_destino': '+57 4 4567890',
            'fecha_inicio': timezone.now() - timedelta(hours=3),
            'fecha_estimada_entrega': timezone.now() + timedelta(hours=5)
        },
        {
            'cliente': clientes[1] if len(clientes) > 1 else None,
            'vehiculo': vehiculos[2] if len(vehiculos) > 2 else None,
            'origen': 'Cali, Colombia',
            'origen_lat': Decimal('3.4516'),
            'origen_lng': Decimal('-76.5320'),
            'destino': 'Barranquilla, Colombia',
            'destino_lat': Decimal('10.9639'),
            'destino_lng': Decimal('-74.7964'),
            'estado': 'en_ruta',
            'prioridad': 'urgente',
            'descripcion_carga': 'Medicamentos y suministros médicos',
            'peso_kg': Decimal('800.00'),
            'valor_declarado': Decimal('120000000.00'),
            'contacto_origen': 'Laboratorio Pharma',
            'telefono_origen': '+57 2 5551234',
            'contacto_destino': 'Hospital del Norte',
            'telefono_destino': '+57 5 3334567',
            'fecha_inicio': timezone.now() - timedelta(hours=6),
            'fecha_estimada_entrega': timezone.now() + timedelta(hours=10)
        },
        {
            'cliente': clientes[2] if len(clientes) > 2 else None,
            'vehiculo': vehiculos[1] if len(vehiculos) > 1 else None,
            'origen': 'Cartagena, Colombia',
            'origen_lat': Decimal('10.3910'),
            'origen_lng': Decimal('-75.4794'),
            'destino': 'Bogotá, Colombia',
            'destino_lat': Decimal('4.7110'),
            'destino_lng': Decimal('-74.0721'),
            'estado': 'pendiente',
            'prioridad': 'media',
            'descripcion_carga': 'Productos alimenticios no perecederos',
            'peso_kg': Decimal('1500.00'),
            'valor_declarado': Decimal('15000000.00'),
            'contacto_origen': 'Distribuidora Costa',
            'telefono_origen': '+57 5 6667890',
            'contacto_destino': 'Supermercado Central',
            'telefono_destino': '+57 1 7778901',
            'fecha_estimada_entrega': timezone.now() + timedelta(days=2)
        },
        {
            'cliente': clientes[0] if len(clientes) > 0 else None,
            'vehiculo': vehiculos[0] if len(vehiculos) > 0 else None,
            'origen': 'Medellín, Colombia',
            'origen_lat': Decimal('6.2476'),
            'origen_lng': Decimal('-75.5658'),
            'destino': 'Bucaramanga, Colombia',
            'destino_lat': Decimal('7.1193'),
            'destino_lng': Decimal('-73.1227'),
            'estado': 'entregado',
            'prioridad': 'baja',
            'descripcion_carga': 'Textiles y confecciones',
            'peso_kg': Decimal('1200.00'),
            'valor_declarado': Decimal('25000000.00'),
            'contacto_origen': 'Fábrica Textil',
            'telefono_origen': '+57 4 8889012',
            'contacto_destino': 'Almacén Santander',
            'telefono_destino': '+57 7 9990123',
            'fecha_inicio': timezone.now() - timedelta(days=2),
            'fecha_entrega': timezone.now() - timedelta(hours=5)
        }
    ]
    
    envios = []
    for data in envios_data:
        # No usar get_or_create porque numero_guia se genera automáticamente
        envio = Envio.objects.create(**data)
        print(f"✅ Envío creado: {envio.numero_guia} - {envio.origen} → {envio.destino}")
        envios.append(envio)
    
    return envios


def crear_eventos(envios):
    print_header("Creando Eventos de Envío")
    
    if len(envios) == 0:
        print("⚠️  No hay envíos para crear eventos")
        return []
    
    eventos = []
    
    # Eventos para el primer envío (en ruta)
    if len(envios) > 0:
        envio = envios[0]
        eventos_data = [
            {
                'envio': envio,
                'tipo': 'inicio',
                'descripcion': 'Carga verificada y envío iniciado desde Bogotá',
                'ubicacion': 'Bogotá, Autopista Norte',
                'latitud': Decimal('4.7110'),
                'longitud': Decimal('-74.0721'),
                'velocidad_kmh': Decimal('0.00'),
                'bateria_dispositivo': 100,
                'fecha': timezone.now() - timedelta(hours=3)
            },
            {
                'envio': envio,
                'tipo': 'checkpoint',
                'descripcion': 'Punto de control - Peaje La Caro',
                'ubicacion': 'Peaje La Caro',
                'latitud': Decimal('4.9500'),
                'longitud': Decimal('-74.0500'),
                'velocidad_kmh': Decimal('75.50'),
                'bateria_dispositivo': 95,
                'fecha': timezone.now() - timedelta(hours=2, minutes=30)
            },
            {
                'envio': envio,
                'tipo': 'parada',
                'descripcion': 'Parada técnica - Estación de servicio',
                'ubicacion': 'Girardot, Estación Terpel',
                'latitud': Decimal('4.3000'),
                'longitud': Decimal('-74.8000'),
                'velocidad_kmh': Decimal('0.00'),
                'bateria_dispositivo': 90,
                'fecha': timezone.now() - timedelta(hours=1, minutes=45)
            },
            {
                'envio': envio,
                'tipo': 'checkpoint',
                'descripcion': 'Aproximándose a destino',
                'ubicacion': 'Entrada a Medellín',
                'latitud': Decimal('6.2000'),
                'longitud': Decimal('-75.5500'),
                'velocidad_kmh': Decimal('65.00'),
                'bateria_dispositivo': 85,
                'fecha': timezone.now() - timedelta(minutes=30)
            }
        ]
        
        for data in eventos_data:
            evento = EventoEnvio.objects.create(**data)
            eventos.append(evento)
            print(f"✅ Evento creado: {evento.get_tipo_display()} - {evento.ubicacion}")
    
    # Eventos para el segundo envío (en ruta urgente)
    if len(envios) > 1:
        envio = envios[1]
        eventos_data = [
            {
                'envio': envio,
                'tipo': 'inicio',
                'descripcion': 'Envío urgente iniciado - Medicamentos',
                'ubicacion': 'Cali, Zona Industrial',
                'latitud': Decimal('3.4516'),
                'longitud': Decimal('-76.5320'),
                'velocidad_kmh': Decimal('0.00'),
                'bateria_dispositivo': 100,
                'fecha': timezone.now() - timedelta(hours=6)
            },
            {
                'envio': envio,
                'tipo': 'checkpoint',
                'descripcion': 'Ruta hacia la costa',
                'ubicacion': 'Buga, Valle del Cauca',
                'latitud': Decimal('3.9000'),
                'longitud': Decimal('-76.3000'),
                'velocidad_kmh': Decimal('80.00'),
                'bateria_dispositivo': 92,
                'fecha': timezone.now() - timedelta(hours=4)
            }
        ]
        
        for data in eventos_data:
            evento = EventoEnvio.objects.create(**data)
            eventos.append(evento)
            print(f"✅ Evento creado: {evento.get_tipo_display()} - {evento.ubicacion}")
    
    return eventos


def crear_alertas(envios):
    print_header("Creando Alertas")
    
    if len(envios) == 0:
        print("⚠️  No hay envíos para crear alertas")
        return []
    
    alertas = []
    
    # Alerta para el segundo envío (urgente)
    if len(envios) > 1:
        alerta = Alerta.objects.create(
            envio=envios[1],
            tipo='velocidad',
            nivel='media',
            descripcion='Velocidad superior a 90 km/h detectada en zona de control'
        )
        alertas.append(alerta)
        print(f"✅ Alerta creada: {alerta.get_tipo_display()} - Nivel {alerta.get_nivel_display()}")
    
    # Alerta crítica para el primer envío
    if len(envios) > 0:
        alerta = Alerta.objects.create(
            envio=envios[0],
            tipo='parada_no_autorizada',
            nivel='alta',
            descripcion='Parada no programada detectada - Duración: 25 minutos'
        )
        alertas.append(alerta)
        print(f"✅ Alerta creada: {alerta.get_tipo_display()} - Nivel {alerta.get_nivel_display()}")
    
    return alertas


def crear_sensores(envios):
    print_header("Creando Datos de Sensores")
    
    if len(envios) == 0:
        print("⚠️  No hay envíos para crear sensores")
        return []
    
    sensores = []
    
    # Sensores para el segundo envío (medicamentos)
    if len(envios) > 1:
        sensores_data = [
            {
                'envio': envios[1],
                'tipo': 'temperatura',
                'valor': '22.5',
                'unidad': '°C',
                'valor_minimo': Decimal('2.0'),
                'valor_maximo': Decimal('8.0')
            },
            {
                'envio': envios[1],
                'tipo': 'humedad',
                'valor': '65',
                'unidad': '%',
                'valor_minimo': Decimal('40.0'),
                'valor_maximo': Decimal('70.0')
            }
        ]
        
        for data in sensores_data:
            sensor = Sensor.objects.create(**data)
            sensores.append(sensor)
            estado = "⚠️ FUERA DE RANGO" if sensor.fuera_de_rango else "✓ Normal"
            print(f"✅ Sensor creado: {sensor.get_tipo_display()} - {sensor.valor} {sensor.unidad} - {estado}")
    
    # Sensores para el primer envío
    if len(envios) > 0:
        sensores_data = [
            {
                'envio': envios[0],
                'tipo': 'vibracion',
                'valor': '2.5',
                'unidad': 'g',
                'valor_minimo': Decimal('0.0'),
                'valor_maximo': Decimal('5.0')
            },
            {
                'envio': envios[0],
                'tipo': 'apertura',
                'valor': 'cerrado',
                'unidad': ''
            }
        ]
        
        for data in sensores_data:
            sensor = Sensor.objects.create(**data)
            sensores.append(sensor)
            print(f"✅ Sensor creado: {sensor.get_tipo_display()} - {sensor.valor}")
    
    return sensores


def main():
    print_header("🚀 CREANDO DATOS DE PRUEBA")
    print("Este script creará usuarios, vehículos, envíos, eventos, alertas y sensores de prueba\n")
    
    try:
        # Crear datos
        admin, clientes, conductores = crear_usuarios()
        vehiculos = crear_vehiculos(conductores)
        envios = crear_envios(clientes, vehiculos)
        eventos = crear_eventos(envios)
        alertas = crear_alertas(envios)
        sensores = crear_sensores(envios)
        
        # Resumen
        print_header("✅ DATOS CREADOS EXITOSAMENTE")
        print(f"""
📊 Resumen:
   - Usuarios: {Usuario.objects.count()} ({Usuario.objects.filter(rol='admin').count()} admin, {Usuario.objects.filter(rol='cliente').count()} clientes, {Usuario.objects.filter(rol='conductor').count()} conductores)
   - Vehículos: {Vehiculo.objects.count()}
   - Envíos: {Envio.objects.count()}
   - Eventos: {EventoEnvio.objects.count()}
   - Alertas: {Alerta.objects.count()}
   - Sensores: {Sensor.objects.count()}

🔐 Credenciales de acceso:
   Admin: admin / admin123
   Cliente: cliente1 / cliente123
   Conductor: conductor1 / conductor123

🌐 Accede al sistema en: http://127.0.0.1:8000/admin/
        """)
        
    except Exception as e:
        print(f"\n❌ Error al crear datos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
