from rest_framework import serializers
from .models import Post, Comment, Library
from users.models import CustomUser
from users.serializers import CustomUserSerializer, UserAuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserAuthorSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content',
                  'created_at', 'updated_at', 'author']
        depth = 1

    def create(self, validated_data):
        author = self.context['request'].user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class PostSerializer(serializers.ModelSerializer):
    author = UserAuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'thumbnail', 'author_id', 'file_upload',
                  'is_anonymous', 'post_type', 'created_at', 'updated_at', 'author', 'comments']

    def create(self, validated_data):
        author = self.context['request'].user
        post = Post.objects.create(author=author, **validated_data)
        return post


class LibrarySerializer(serializers.ModelSerializer):
    author = UserAuthorSerializer(read_only=True)

    class Meta:
        model = Library
        fields = ['id', 'title', 'content', 'file_upload', 'is_anonymous', 'created_at', 'updated_at', 'author']

    def create(self, validated_data):
        author = self.context['request'].user
        library = Library.objects.create(author=author, **validated_data)
        return library