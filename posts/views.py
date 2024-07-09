from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from posts.serializers import (
    CategoryReadSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer
)
from .models import Category, Post, Comment
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsAuthorOrReadOnly
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve post categories
    """
    
    queryset = Category.objects.all()
    serializer_class = CategoryReadSerializer
    permission_classes = (permissions.AllowAny,)
    
class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD on Posts
    """
    
    queryset = Post.objects.all()
    
    
    #In order to user different serializers for different
    #actions, we can override get_serializer_class(self)
    def get_serializer_class(self):
        if self.action in ("create", "udpate", "partial_update","destroy"):
            return PostWriteSerializer
        return PostReadSerializer 

    # get_permissions(self) method helps you separate
    # permissions for different actions inside the same view
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action is ("update", "partial_udpate", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)
        
        return super().get_permissions()
    

class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD comments for a particular set
    """
    
    queryset = Comment.objects.all()
    
    def get_queryset(self):
        res = super().get_queryset()
        post_id = self.kwargs.get("post_id")
        return res.filter(post__id = post_id)


    def get_serializer_class(self):
        if self.action in ("create", "upadate","partial_update","destroy"):
            return CommentWriteSerializer
        return CommentReadSerializer
    
    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()

class LikePostAPIView(APIView):
    """
    Like, Dislike a POST
    """
    permission_classes = (permissions.IsAuthenticated,)
    
    
    def get(self, request, post_primarykey):
        user = request.user
        post = get_object_or_404(Post, post_primarykey)
        
        if user in post.likes.all():
            post.likes.remove(user)
        
        else:
            post.likes.add(user)
        
        return Response(status=status.HTTP_200_OK)