import json
import pytest
from chat.consumers import ChatConsumer
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.testing import WebsocketCommunicator
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from .models import ChatRoom, Message


class MessageViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.user1 = CustomUser.objects.create_user(
            password='testpass123', email='whoisdinanath@gmail.com')
        self.user2 = CustomUser.objects.create_user(
            password='testpass123', email='test2@email.com')

        # Create chat room
        self.chat_room = ChatRoom.objects.create(
            participant1=self.user1, participant2=self.user2)

        # Create messages
        Message.objects.create(content='Hello, user2!',
                               chat_room=self.chat_room, sender=self.user1)
        Message.objects.create(content='Hello, user1!',
                               chat_room=self.chat_room, sender=self.user2)

        # Get JWT token for user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
# router.register(r'(?P<chat_room_id>\d+)/messages',
        # MessageViewSet, basename='messages')

    def test_list_messages(self):
        response = self.client.get(
            reverse('messages-list', kwargs={'chat_room_id': self.chat_room.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_message(self):
        response = self.client.post(reverse('messages-list', kwargs={'chat_room_id': self.chat_room.id}), {
                                    'content': 'New message!', 'chat_room': self.chat_room.id, 'sender': self.user1.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 3)


# Define the application for the test
application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(
            r'ws/chat/(?P<userId>\w+)/(?P<otherUserId>\w+)/$',
            ChatConsumer.as_asgi()
        ),
    ])
})

# Define the test


@pytest.mark.asyncio
async def test_chat_consumer():
    # Create a WebsocketCommunicator instance for the consumer
    communicator = WebsocketCommunicator(application, '/ws/chat/user1/user2/')

    # Connect to the consumer
    connected, _ = await communicator.connect()
    assert connected

    # Send a message to the consumer
    await communicator.send_to(text_data=json.dumps({
        'action': 'new_message',
        'message': 'Hello, world!',
        'chat_room': 'room1',
        'other_user': 'user2',
        'sender': 'user1'
    }))

    # Receive the message the consumer
    response = await communicator.receive_from()

    # Load the response data
    response_data = json.loads(response)

    # Check the content of the response
    assert response_data['action'] == 'new_message'
    assert response_data['content'] == 'Hello, world!'
    assert response_data['chat_room'] == 'room1'
    assert response_data['sender'] == 'user1'

    # Disconnect from the consumer
    await communicator.disconnect()
