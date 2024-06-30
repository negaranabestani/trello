from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["query_string"].decode().split("=")[1]
        # self.user = self.scope["user"]
        # if not self.user.is_authenticated:
        #     await self.accept()
        #     await self.send(text_data=json.dumps({'message': 'You are not authenticated.'}))
        #     await self.disconnect(403)
        #     return

        self.group_name = f"user_{self.user_id}"

        # Add user to the group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.close(403, close_code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({'message': data}))

    async def send_message(self, event):
        message = event['message']
        await self.send(text_data=message)
