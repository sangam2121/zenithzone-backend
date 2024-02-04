from django.db import models
from users.models import CustomUser
import uuid


# Create your models here.
post_type = (
    ("DAILY_UPDATES", "Daily Updates"),
    ("INSPIRATIONAL", "Inspirational"),
    ("EXPERT_ADVICE", "Expert Advice"),
    ("NEWS", "News"),
    ("OTHERS", "Others")
)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    thumbnail = models.ImageField(
        upload_to='posts/thumbnails', default='posts/images/default.png')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='posts')
    file_upload = models.FileField(
        upload_to='posts/files', null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    post_type = models.CharField(max_length=100, choices=post_type)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    @property
    def anonymous(self):
        return self.is_anonymous

    @property
    def get_post_type(self):
        return self.post_type

    @property
    def get_name(self):
        if self.is_anonymous:
            return "Anonymous Participant"
        else:
            return self.author.first_name + ' ' + self.author.last_name

    @property
    def get_comments(self):
        return self.comment_set.all()

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.first_name + "_" + self.post.title

    class Meta:
        verbose_name_plural = 'Comments'
        unique_together = ('post', 'author')
        ordering = ['-created_at']

    @property
    def get_name(self):
        return self.author.first_name + ' ' + self.author.last_name
