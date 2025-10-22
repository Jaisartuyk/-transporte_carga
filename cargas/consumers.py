"""
WebSocket Consumers para rastreo GPS en tiempo real
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GPSTrackingConsumer(AsyncWebsocketConsumer):
    """
    Consumer para rastreo GPS en tiempo real
    Permite que múltiples usuarios vean actualizaciones de un envío
    """
    
    async def connect(self):
        """
        Llamado cuando el WebSocket se conecta
        """
        # Obtener el ID del envío de la URL
        self.envio_id = self.scope['url_route']['kwargs']['envio_id']
        self.room_group_name = f'tracking_{self.envio_id}'
        
        # Verificar autenticación
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        # Unirse al grupo del envío
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Aceptar la conexión
        await self.accept()
        
        # Enviar mensaje de confirmación
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Conectado al rastreo del envío {self.envio_id}'
        }))
    
    async def disconnect(self, close_code):
        """
        Llamado cuando el WebSocket se desconecta
        """
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Recibir mensaje del WebSocket (opcional)
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'ping':
                # Responder a ping
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
        except json.JSONDecodeError:
            pass
    
    async def gps_update(self, event):
        """
        Recibir actualización GPS del grupo y enviarla al WebSocket
        """
        # Enviar mensaje al WebSocket del cliente
        await self.send(text_data=json.dumps({
            'type': 'gps_update',
            'data': event['data']
        }))
    
    async def envio_status_update(self, event):
        """
        Recibir actualización de estado del envío
        """
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'data': event['data']
        }))
