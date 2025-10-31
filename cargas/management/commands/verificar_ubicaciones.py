from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cargas.models import EventoEnvio, Envio, Vehiculo, Usuario

class Command(BaseCommand):
    help = 'Verifica las ubicaciones GPS registradas en la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('VERIFICACIÓN DE UBICACIONES GPS'))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))
        
        # 1. Total de eventos GPS
        total_eventos = EventoEnvio.objects.filter(
            latitud__isnull=False,
            longitud__isnull=False
        ).count()
        self.stdout.write(f"📍 Total de eventos GPS registrados: {total_eventos}")
        
        # 2. Eventos de las últimas 24 horas
        hace_24_horas = timezone.now() - timedelta(hours=24)
        eventos_recientes = EventoEnvio.objects.filter(
            latitud__isnull=False,
            longitud__isnull=False,
            fecha__gte=hace_24_horas
        ).order_by('-fecha')
        
        self.stdout.write(f"🕐 Eventos de las últimas 24 horas: {eventos_recientes.count()}\n")
        
        if eventos_recientes.exists():
            self.stdout.write(self.style.SUCCESS("Últimos 10 eventos GPS:"))
            self.stdout.write("-" * 80)
            
            for evento in eventos_recientes[:10]:
                conductor = "Sin conductor"
                vehiculo = "Sin vehículo"
                
                if evento.envio and evento.envio.vehiculo:
                    vehiculo = evento.envio.vehiculo.placa
                    if evento.envio.vehiculo.conductor:
                        conductor = evento.envio.vehiculo.conductor.nombre_completo
                
                self.stdout.write(
                    f"  • {evento.fecha.strftime('%Y-%m-%d %H:%M:%S')} | "
                    f"Conductor: {conductor} | "
                    f"Vehículo: {vehiculo} | "
                    f"Envío: {evento.envio.numero_guia if evento.envio else 'N/A'} | "
                    f"Estado: {evento.envio.get_estado_display() if evento.envio else 'N/A'} | "
                    f"Coords: ({evento.latitud}, {evento.longitud})"
                )
        else:
            self.stdout.write(self.style.WARNING("⚠️  No hay eventos GPS en las últimas 24 horas"))
        
        # 3. Envíos activos
        self.stdout.write("\n" + "="*80)
        envios_activos = Envio.objects.exclude(
            estado__in=['entregado', 'cancelado']
        ).select_related('vehiculo', 'vehiculo__conductor')
        
        self.stdout.write(f"📦 Envíos activos (no entregados/cancelados): {envios_activos.count()}")
        
        if envios_activos.exists():
            self.stdout.write("\nDetalle de envíos activos:")
            self.stdout.write("-" * 80)
            
            for envio in envios_activos:
                conductor = "Sin conductor"
                vehiculo = "Sin vehículo"
                
                if envio.vehiculo:
                    vehiculo = envio.vehiculo.placa
                    if envio.vehiculo.conductor:
                        conductor = envio.vehiculo.conductor.nombre_completo
                
                # Contar eventos GPS de este envío
                eventos_gps = EventoEnvio.objects.filter(
                    envio=envio,
                    latitud__isnull=False,
                    longitud__isnull=False
                ).count()
                
                # Último evento
                ultimo_evento = EventoEnvio.objects.filter(
                    envio=envio,
                    latitud__isnull=False,
                    longitud__isnull=False
                ).order_by('-fecha').first()
                
                ultima_actualizacion = "Nunca"
                if ultimo_evento:
                    ultima_actualizacion = ultimo_evento.fecha.strftime('%Y-%m-%d %H:%M:%S')
                
                self.stdout.write(
                    f"  • Guía: {envio.numero_guia} | "
                    f"Estado: {envio.get_estado_display()} | "
                    f"Conductor: {conductor} | "
                    f"Vehículo: {vehiculo} | "
                    f"GPS: {eventos_gps} eventos | "
                    f"Última: {ultima_actualizacion}"
                )
        
        # 4. Conductores activos
        self.stdout.write("\n" + "="*80)
        conductores = Usuario.objects.filter(rol='conductor', is_active=True)
        self.stdout.write(f"👤 Conductores activos: {conductores.count()}")
        
        if conductores.exists():
            self.stdout.write("\nDetalle de conductores:")
            self.stdout.write("-" * 80)
            
            for conductor in conductores:
                # Buscar vehículo asignado
                vehiculo = Vehiculo.objects.filter(conductor=conductor).first()
                
                # Buscar envíos del conductor
                envios_conductor = Envio.objects.filter(
                    vehiculo__conductor=conductor
                ).exclude(estado__in=['entregado', 'cancelado'])
                
                # Contar eventos GPS del conductor
                eventos_conductor = EventoEnvio.objects.filter(
                    envio__vehiculo__conductor=conductor,
                    latitud__isnull=False,
                    longitud__isnull=False,
                    fecha__gte=hace_24_horas
                ).count()
                
                self.stdout.write(
                    f"  • {conductor.nombre_completo} | "
                    f"Vehículo: {vehiculo.placa if vehiculo else 'Sin asignar'} | "
                    f"Envíos activos: {envios_conductor.count()} | "
                    f"GPS (24h): {eventos_conductor} eventos"
                )
        
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.SUCCESS("✅ Verificación completada\n"))
