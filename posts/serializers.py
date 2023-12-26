from rest_framework import serializers
from .models import Post, Comment
from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'author']
        depth = 1

    def create(self, validated_data):
        user = self.context['request'].user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    # author_id = serializers.PrimaryKeyRelatedField(
    #     queryset=CustomUser.objects.all(), source='author')
    # author = serializers.ReadOnlyField(source='author.email')
    author = CustomUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'thumbnail', 'author_id',
                  'is_anonymous', 'post_type', 'created_at', 'updated_at', 'author', 'comments']

    def create(self, validated_data):
        author = self.context['request'].user
        print(author)
        post = Post.objects.create(author=author, **validated_data)
        return post
