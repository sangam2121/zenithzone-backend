from django.shortcuts import render
from users.models import CustomUser
from .models import ChatRoom, Message
from rest_framework import generics
from .serializers import MessageSerializer, ChatRoomSerializer, ChatRoomListSerializer, MessageListSerializer
from rest_framework import viewsets
from rest_framework.response import Response
# Q
from django.db.models import Q
from rest_framework import status
# get or create chat room



class ChatRoomCreateAPIView(generics.CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def perform_create(self, serializer):
        participant1 = serializer.validated_data['participant1']
        participant2 = serializer.validated_data['participant2']

        if participant1 != self.request.user and participant2 != self.request.user:
            raise PermissionError("You are not allowed to create chat room.")

        chat_room, created = ChatRoom.objects.get_or_create(
            participant1=participant1,
            participant2=participant2,
            defaults={'participant1': participant1, 'participant2': participant2}
        )

        if created:
            serializer.save()
        else:
            raise ValidationError("Chat room already exists.")

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'Chat room created successfully',
                'chat_room': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Chat room could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

class ChatRoomListAPIView(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomListSerializer

    def get_queryset(self):
        queryset = ChatRoom.objects.all().filter()
        queryset = queryset.filter(
                Q(participant1=self.request.user) | Q(participant2=self.request.user))
        participant = self.request.query_params.get('participant', None)
        if participant is not None:
            queryset = queryset.filter(Q(participant1=participant) | Q(participant2=participant))
        return queryset

class ChatRoomUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.participant1 != self.request.user and instance.participant2 != self.request.user:
            raise PermissionError

    def perform_destroy(self, instance):
        if instance.participant1 == self.request.user or instance.participant2 == self.request.user:
            instance.delete()
        else:
            raise PermissionError

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Chat room updated successfully',
                'chat_room': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not a participant in this chat room.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Chat room could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Chat room deleted successfully',
                'chat_room': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not a participant in this chat room.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Chat room could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)



class MessageCreateAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        if serializer.validated_data['sender'] != self.request.user:
            raise PermissionError("You are not allowed to create message.")
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'Message created successfully',
                'message': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Message could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

class MessageListAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        queryset = queryset.filter(
                Q(chat_room__participant1=self.request.user) | Q(chat_room__participant2=self.request.user))
        chat_room = self.request.query_params.get('chat_room', None)
        if chat_room is not None:
            queryset = queryset.filter(chat_room=chat_room)
        return queryset

class MessageUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.sender != self.request.user:
            raise PermissionError

    def perform_destroy(self, instance):
        if instance.sender == self.request.user:
            instance.delete()
        else:
            raise PermissionError

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Message updated successfully',
                'message': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not the author of this message.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Message could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Message deleted successfully',
                'message': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not the author of this message.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Message could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)