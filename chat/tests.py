from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ChatRoom, Message


class ChatRoomMessageTestCase(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = get_user_model().objects.create_user(
            email='user1@example.com',
            first_name='John',
            last_name='Doe',
            password='password1',
            phone='123-456-7890',
            address='123 Main St',
            bio='A brief bio about user1',
            user_type='doctor'
        )

        self.user2 = get_user_model().objects.create_user(
            email='user2@example.com',
            first_name='Jane',
            last_name='Doe',
            password='password2',
            phone='987-654-3210',
            address='456 Oak St',
            bio='A brief bio about user2',
            user_type='patient'
        )

    def test_create_and_retrieve_chat_room(self):
        # Create a chat room
        response = self.client.post(
            '/api/chat/rooms', data={'members': [str(self.user1.id), str(self.user2.id)]}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve the created chat room
        response = self.client.get(
            f'/api/chat/rooms/{str(self.user1.id)}/{str(self.user2.id)}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected structure
        expected_data = {
            'id': response.data['id'],
            'user1': str(self.user1.id),
            'user2': str(self.user2.id),
            'participants': [
                {'id': str(self.user1.id), 'username': 'user1'},
                {'id': str(self.user2.id), 'username': 'user2'}
            ]
            # Add other expected fields based on your serializer
        }

        self.assertEqual(response.data, expected_data)

    def test_create_and_retrieve_messages(self):
        # Create a chat room
        response = self.client.post(
            '/api/chat/rooms', data={'members': [str(self.user1.id), str(self.user2.id)]}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        chat_room_id = response.data['id']

        # Create a message in the chat room
        response = self.client.post(
            f'/api/chat/messages/{chat_room_id}', data={'content': 'Hello'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve messages in the chat room
        response = self.client.get(
            f'/api/chat/messages/{chat_room_id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data matches the expected structure
        expected_data = [
            {
                'id': response.data[0]['id'],
                'content': 'Hello',
                'chat_room': str(chat_room_id),
                'sender': str(self.user1.id)
                # Add other expected fields based on your serializer
            }
        ]

        self.assertEqual(response.data, expected_data)
