from django.shortcuts import render
from users.models import CustomUser
from .models import Chat
from rest_framework import generics


from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        chatroom_id = self.request.query_params.get('chatroom', None)
        if chatroom_id is not None:
            queryset = queryset.filter(chatroom_id=chatroom_id)
        return queryset
