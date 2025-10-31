from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import Envio, EventoEnvio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recibir_ubicacion(request):
    """
    API para recibir ubicaciones GPS de conductores
    """
    try:
        # Obtener datos de la ubicación
        lat = request.data.get('lat')
        lng = request.data.get('lng')
        accuracy = request.data.get('accuracy')
        speed = request.data.get('speed')
        heading = request.data.get('heading')
        timestamp = request.data.get('timestamp')
        
        # Validar datos requeridos
        if not lat or not lng:
            return Response(
                {'error': 'Latitud y longitud son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el usuario sea conductor
        if request.user.rol != 'conductor':
            return Response(
                {'error': 'Solo los conductores pueden enviar ubicaciones'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener envío activo del conductor
        envio = Envio.objects.filter(
            vehiculo__conductor=request.user,
            estado='en_ruta'
        ).first()
        
        if not envio:
            return Response(
                {'error': 'No tienes envíos activos'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Crear evento de ubicación
        evento = EventoEnvio.objects.create(
            envio=envio,
            ubicacion=f"GPS: {lat}, {lng}",
            latitud=lat,
            longitud=lng,
            fecha=now()
        )
        
        # No actualizamos campos que no existen en el modelo
        # En su lugar, usamos el último evento de ubicación
        
        # Enviar actualización por WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'tracking_{envio.id}',
            {
                'type': 'gps_update',
                'data': {
                    'lat': float(lat),
                    'lng': float(lng),
                    'fecha': evento.fecha.isoformat(),
                    'accuracy': accuracy,
                    'speed': speed,
                    'heading': heading,
                    'conductor': request.user.get_full_name(),
                    'vehiculo': envio.vehiculo.placa
                }
            }
        )
        
        return Response({
            'success': True,
            'message': 'Ubicación recibida y transmitida',
            'evento_id': evento.id,
            'envio': envio.numero_guia
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sincronizar_ubicaciones(request):
    """
    API para sincronizar múltiples ubicaciones pendientes
    """
    try:
        ubicaciones = request.data.get('ubicaciones', [])
        
        if not ubicaciones:
            return Response(
                {'error': 'No hay ubicaciones para sincronizar'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el usuario sea conductor
        if request.user.rol != 'conductor':
            return Response(
                {'error': 'Solo los conductores pueden enviar ubicaciones'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Obtener envío activo del conductor
        envio = Envio.objects.filter(
            vehiculo__conductor=request.user,
            estado='en_ruta'
        ).first()
        
        if not envio:
            return Response(
                {'error': 'No tienes envíos activos'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Crear eventos para cada ubicación
        eventos_creados = 0
        for ubicacion in ubicaciones:
            lat = ubicacion.get('lat')
            lng = ubicacion.get('lng')
            
            if lat and lng:
                EventoEnvio.objects.create(
                    envio=envio,
                    ubicacion=f"GPS: {lat}, {lng}",
                    latitud=lat,
                    longitud=lng,
                    fecha=ubicacion.get('timestamp', now())
                )
                eventos_creados += 1
        
        # No actualizamos campos que no existen en el modelo
        # El último evento de ubicación se puede obtener con una consulta
        
        return Response({
            'success': True,
            'message': f'{eventos_creados} ubicaciones sincronizadas',
            'envio': envio.numero_guia
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
