from rest_framework import serializers
from .models import ChatRoom, Message
from users.serializers import CustomUserSerializer
from users.models import CustomUser


# class ChatRoomSerializer(serializers.ModelSerializer):
#     participants = CustomUserSerializer(many=True, read_only=True)
#     members = serializers.ListField(write_only=True)

#     def create(self, validated_data):
#         members = validated_data.pop('members')

#         # Ensure that the chat room is created uniquely for the pair of users
#         participant1 = members[0]
#         participant2 = members[1]
#         chatroom, created = ChatRoom.objects.get_or_create(
#             user1=participant1, user2=participant2)

#         return chatroom

#     class Meta:
#         model = ChatRoom
#         fields = '__all__'


# class MessageSerializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField()
#     # get from doctor or patient
#     # user_image = serializers.ImageField( read_only=True)

#     class Meta:
#         model = Message
#         fields = ['id', 'chat_room', 'sender',
#                   'username', 'content', 'created_at']

#     def get_username(self, obj):
#         return obj.sender.first_name + " " + obj.sender.last_name


class ChatRoomSerializer(serializers.ModelSerializer):
    participant1 = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
    participant2 = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())

    class Meta:
        model = ChatRoom
        fields = ['id', 'participant1', 'participant2']

class ChatRoomListSerializer(serializers.ModelSerializer):
    participant1 = CustomUserSerializer()
    participant2 = CustomUserSerializer()

    class Meta:
        model = ChatRoom
        fields = ['id', 'participant1', 'participant2']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['participant1'] = CustomUserSerializer(instance.participant1).data
        data['participant2'] = CustomUserSerializer(instance.participant2).data
        return data





class MessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    # get from doctor or patient
    # user_image = serializers.ImageField( read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender',
                  'username', 'content', 'created_at']

    def get_username(self, obj):
        return obj.sender.first_name + " " + obj.sender.last_name


class MessageListSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer()
    chat_room = ChatRoomListSerializer()

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender',
                  'content', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sender'] = CustomUserSerializer(instance.sender).data
        return data