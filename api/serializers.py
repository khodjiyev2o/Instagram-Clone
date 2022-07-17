from rest_framework import serializers
from users.models import User
from main.models import Post,Follow,Comment



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "is_admin", "username", "first_name", "last_name", "email"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','posted','owner','description','likes']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"