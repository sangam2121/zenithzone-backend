from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, user_id, other_user_id):
        # Ensure that the chat room is unique for the pair of users
        room_names = sorted([user_id, other_user_id])
        chatroom = ChatRoom.objects.filter(
            user1=room_names[0], user2=room_names[1]).first()

        if not chatroom:
            return Response({"detail": "Chat room not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatRoomSerializer(chatroom, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id, other_user_id):
        # Ensure that the chat room is created uniquely for the pair of users
        room_names = sorted([user_id, other_user_id])
        request.data['members'] = room_names
        serializer = ChatRoomSerializer(
            data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageView(ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs['chatroom_id']
        return Message.objects.filter(chat_room=chatroom_id)
