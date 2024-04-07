from rest_framework import serializers
from .models import ChatRoom, Message
from users.serializers import CustomUserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    # participants = CustomUserSerializer(many=True, read_only=True)
    participant1 = CustomUserSerializer(read_only=True)
    participant2 = CustomUserSerializer(read_only=True)
    members = serializers.ListField(write_only=True)
    pp1 = serializers.SerializerMethodField()
    pp2 = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()


    def get_pp1(self, obj):
        if obj.participant1.user_type == 'doctor':
            return obj.participant1.doctor.image.url
        elif obj.participant1.user_type == 'patient':
            return obj.participant1.patient.image.url
        #return none if the user is not a doctor or patient
        return None

    def get_pp2(self, obj):
        if obj.participant2.user_type == 'doctor':
            return obj.participant2.doctor.image.url
        elif obj.participant1.user_type == 'patient':
            return obj.participant1.patient.image.url
        #return none if the user is not a doctor or patient
        return None
        
    def get_last_message(self, obj):
        try:
            message = Message.objects.filter(chat_room=obj).latest('created_at')
            return MessageSerializer(message).data
        except:
            return None

    

    def create(self, validated_data):
        members = validated_data.pop('members')

        # Ensure that the chat room is created uniquely for the pair of users
        participant1 = members[0]
        participant2 = members[1]
        chatroom, created = ChatRoom.objects.get_or_create(
            user1=participant1, user2=participant2)

        return chatroom

    class Meta:
        model = ChatRoom
        fields = '__all__'


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