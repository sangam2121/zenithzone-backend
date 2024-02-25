from django.shortcuts import render
from users.models import CustomUser
from .models import ChatRoom, Message
from rest_framework import generics
from .serializers import MessageSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class MessageViewSet(viewsets.ViewSet):
    def list(self, request, chat_room_id=None):
        queryset = Message.objects.filter(chat_room_id=chat_room_id)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, chat_room_id=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
