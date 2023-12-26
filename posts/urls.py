from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', PostListAPIView.as_view(), name='post-list'),
    path('details/<slug:pk>/', PostUpdateAPIView.as_view(), name='post-update'),
    path('delete/<slug:pk>/', PostDeleteAPIView.as_view(), name='post-delete'),

    path('comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/details/<slug:pk>/', CommentUpdateAPIView.as_view(),
         name='comment-update'),
    path('comments/delete/<slug:pk>/',
         CommentDeleteAPIView.as_view(), name='comment-delete'),
]
