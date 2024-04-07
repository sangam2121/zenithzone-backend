import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from users.models import CustomUser
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    def getUser(self, userId):
        return CustomUser.objects.filter(id=userId).first()

    def saveMessage(self, message, chat_room_id, sender_id):
        sender_id = self.userId
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

    def getMessageData(self, message):
        return {
            "id": str(message.id),
            "chat_room": str(message.chat_room.id),
            "sender": str(message.sender.id),
            "content": message.content,
            "created_at": message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    async def connect(self):
        ############ AUTHENTICATION ############
        # self.user = self.scope["user"]
        # if self.user.is_authenticated:
        #     print(f"User {self.user} is authenticated")
        #     pass
        # else:
        #     print("User is not authenticated")
        #     await self.close()
        ############ CONNECTION  INITIALIZATION ############
        self.userId = self.scope['url_route']['kwargs']['userId']
        self.otherUserId = self.scope['url_route']['kwargs']['otherUserId']

        # Ensure that the room name is unique for the pair of users
        room_names = sorted([self.userId, self.otherUserId])
        self.room_group_name = f'chat_{room_names[0]}_{room_names[1]}'

        ####### GET OR CREATE CHAT ROOM ########
        participant1, participant2 = sorted([self.userId, self.otherUserId])

        participant1 = await sync_to_async(CustomUser.objects.get, thread_sensitive=True)(pk=participant1)
        participant2 = await sync_to_async(CustomUser.objects.get, thread_sensitive=True)(pk=participant2)
        print(f"Participant1: {participant1}")

        self.chat_room, created = await sync_to_async(ChatRoom.objects.get_or_create, thread_sensitive=True)(
                    participant1=participant1, participant2=participant2)
        chat_room_id = self.chat_room.id


        ####### SEND CHAT ROOM ID TO CLIENT ########
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # Send the chat room ID to the client
        await self.send(text_data=json.dumps({
            'connected': True,
            'chat_room_id': str(self.chat_room.id),
        }))
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            print(f"Text data: {text_data}")
        action = data['action']
        chat_room_id = self.chat_room.id
        other_user_id = self.otherUserId
        chatMessage = {}

        ################### NEW MESSAGE ###################
        if action == 'new_message':
            message = data['message']
            sender_id = self.userId
            if self.userId == self.otherUserId:
                chatMessage = await database_sync_to_async(self.saveMessage)(
                    message, chat_room_id, sender_id)
            chatMessage = await database_sync_to_async(self.saveMessage)(
                message, chat_room_id, sender_id)

        ################### TYPING ###################
        elif action == 'typing':
            chatMessage = data
            chatMessage['action'] = 'typing'

        elif action == 'not_typing':
            chatMessage = data
            chatMessage['action'] = 'not_typing'

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chatMessage
            }
        )

    ################### CHAT MESSAGE ###################
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))