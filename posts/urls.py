from django.urls import path
from rest_framework import routers
from .views import *
from django.conf.urls import include


router = routers.DefaultRouter()
router.register(r'library', LibraryViewSet)

urlpatterns = [
     path('', include(router.urls)),
    path('lists', PostListAPIView.as_view(), name='post-list'),
    path('update/<slug:pk>/', PostUpdateAPIView.as_view(), name='post-update'),
    path('delete/<slug:pk>/', PostDeleteAPIView.as_view(), name='post-delete'),

    path('comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/update/<slug:pk>/', CommentUpdateAPIView.as_view(),
         name='comment-update'),
    path('comments/delete/<slug:pk>/',
         CommentDeleteAPIView.as_view(), name='comment-delete'),
]
