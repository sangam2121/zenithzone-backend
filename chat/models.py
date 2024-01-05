from django.db import models
from users.models import CustomUser
import uuid

# Create your models here.


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1000)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.first_name + ' ' + self.sender.last_name + ' to ' + self.receiver.first_name + ' ' + self.receiver.last_name

    class Meta:
        verbose_name_plural = 'Chats'
        ordering = ['-timestamp']
