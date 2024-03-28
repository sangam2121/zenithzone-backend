# from django.db import models
# from users.models import CustomUser
# import uuid
# from django.conf import settings

# # Create your models here.


# class ChatRoom(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     participant1 = models.ForeignKey(
#         CustomUser, related_name='user1', on_delete=models.CASCADE)
#     participant2 = models.ForeignKey(
#         CustomUser, related_name='user2', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.participant1} - {self.participant2}"

#     def save(self, *args, **kwargs):
#         if self.participant1 == self.participant2:
#             raise ValueError(
#                 'A chat room must have two distinct participants')
#         if ChatRoom.objects.filter(participant1=self.participant2, participant2=self.participant1).exists():
#             raise ValueError(
#                 'A chat room already exists for these participants')
#         super().save(*args, **kwargs)

#     class Meta:
#         unique_together = ('participant1', 'participant2')
#         ordering = ('participant1', 'participant2')


# class Message(models.Model):
#     """
#     This class represents the message model.
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     chat_room = models.ForeignKey(
#         ChatRoom, related_name='messages', on_delete=models.CASCADE)
#     sender = models.ForeignKey(
#         CustomUser, related_name='messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('created_at', )

#     def __str__(self):
#         return f"{self.sender} - {self.chat_room}"

#     def save(self, *args, **kwargs):
#         if self.sender != self.chat_room.participant1 and self.sender != self.chat_room.participant2:
#             raise ValueError('The message sender must be a participant in the chat room')

#         super().save(*args, **kwargs)


from django.db import models
from users.models import CustomUser
import uuid
from django.conf import settings

# Create your models here.


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant1 = models.ForeignKey(
        CustomUser, related_name='user1', on_delete=models.CASCADE)
    participant2 = models.ForeignKey(
        CustomUser, related_name='user2', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.participant1} - {self.participant2}"


class Message(models.Model):
    """
    This class represents the message model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(
        ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        CustomUser, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )