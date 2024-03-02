from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = Post.objects.all()
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__user__name__istartswith=author)
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__istartswith=title)
        post_type = self.request.query_params.get('post_type', None)
        if post_type is not None:
            queryset = queryset.filter(post_type__istartswith=post_type)        
        return queryset 

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.data = {
                'message': 'Post created successfully',
                'post': response.data
            }
            return response
        except Exception as e:
            return Response({'error': 'Post could not be created: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # if not author, raise permission error
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.author != self.request.user:
            raise PermissionError(
                'You are not allowed to update this post'
            )
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Post updated successfully',
                'post': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not the author of this post.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Post could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
        else:
            raise PermissionError

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Post deleted successfully',
                'post': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not the author of this post.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Post could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all()
        post = self.request.query_params.get('post', None)
        if post is not None:
            queryset = queryset.filter(post__id=post)
        return queryset


class CommentUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.user != self.request.user:
            raise PermissionError

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data = {
                'message': 'Comment updated successfully',
                'comment': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not the author of this comment.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Comment could not be updated: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
        else:
            raise PermissionError

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            response.data = {
                'message': 'Comment deleted successfully',
                'comment': response.data
            }
            return response
        except PermissionError as e:
            return Response({'error': 'You are not the author of this comment.', 'status': f'{status.HTTP_403_FORBIDDEN}'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Comment could not be deleted: {}'.format(str(e)), 'status': f'{status.HTTP_400_BAD_REQUEST}'}, status=status.HTTP_400_BAD_REQUEST)
