from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
import asyncio

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("driverpool",self.channel_name)

    async def disconnect(self):
        await self.channel_layer.group_discard("driverpool",self.channel_name)

    async def user_notification(self, event):
        await self.send_json(event)
        print(f"Intercept {event} at {self.channel_name}")


    
