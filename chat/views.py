from django.shortcuts import render
from users.models import CustomUser
from .models import ChatRoom, Message
from rest_framework import generics
from .serializers import MessageSerializer, ChatRoomSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework import permissions


class MessageListAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = Message.objects.all()
        try:
            queryset = queryset.filter(
                    Q(chat_room__participant1=self.request.user) | Q(chat_room__participant2=self.request.user))

        except:
            queryset = Message.objects.none()
        chat_id = self.request.query_params.get('chat_room', None)
        if chat_id is not None:
            queryset = queryset.filter(Q(
                chat_room__id=chat_id
            ))

        return queryset



class ChatRoomListAPIView(generics.ListAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(participant1=self.request.user) | Q(participant2=self.request.user))

        participant = self.request.query_params.get('participant', None)
        if participant is not None:
            queryset = queryset.filter(Q(participant1=participant) | Q(participant2=participant))

        participant_name = self.request.query_params.get('participant_name', None)
        if participant_name is not None:
            queryset = queryset.filter(Q(participant1__first_name=participant_name) | Q(participant2__first_name=participant_name) | Q(participant1__last_name=participant_name) | Q(participant2__last_name=participant_name))

        return queryset