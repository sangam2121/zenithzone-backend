import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    def getUser(self, userId):
        return CustomUser.objects.filter(id=userId).first()

    # def getOnlineUsers(self):
        # return CustomUser.objects.filter(is_online=True)

    def saveMessage(self, message, chat_room_id, sender_id):
        user = CustomUser.objects.get(id=sender_id)
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        message = Message.objects.create(
            content=message, chat_room=chat_room, sender=user)

        return {
            "action": "new_message",
            "id": str(message.id),
            "chat_room": str(message.chat_room.id),
            "sender": str(message.sender.id),
            "content": message.content,
            "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    async def connect(self):
        self.userId = self.scope['url_route']['kwargs']['userId']
        otherUserId = self.scope['url_route']['kwargs']['otherUserId']

        # Ensure that the room name is unique for the pair of users
        room_names = sorted([self.userId, otherUserId])
        self.room_group_name = f'chat_{room_names[0]}_{room_names[1]}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        room_id = data['chat_room']
        other_user_id = data['other_user']
        chatMessage = {}

        # ...

        if action == 'new_message':
            message = data['message']
            sender_id = data['sender']

            # Create or get the chat room
            chat_room, created = ChatRoom.objects.get_or_create(
                user1=self.userId, user2=other_user_id)

            chatMessage = await database_sync_to_async(self.saveMessage)(
                message, chat_room.id, sender_id)
        elif action == 'typing':
            chatMessage = data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chatMessage
            }
        )
    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
