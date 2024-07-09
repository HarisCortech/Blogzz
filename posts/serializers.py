from rest_framework import serializers
from .models import Comment, Post, Category

class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class PostReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    categories = serializers.SerializerMethodField(read_only = True)
    likes = serializers.SerializerMethodField(read_only = True)
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Post
        fields = "__all__"
        
    def get_categories(self, obj):
        categories = list(
            cat.name for cat in obj.categories.all().only("name")
        )
        return categories
    
    def get_likes(self, obj):
        likes = list(
            like.username for like in obj.likes.all().only('username')
        )
        return likes
    
class PostWriteSerializer(serializers.ModelSerializer):
    
    # HiddenField: we dont need to define author in the request
    # CurrentUserDefault: Makes sure the current user/the owner is creating or updating this post
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Post
        fields = "__all__"

class CommentReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source = "author.username", read_only=True)
    
    class Meta:
        model = Comment
        fields  = "__all__"

class CommentWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = "__all__"

