from rest_framework import serializers

from .models import Post, Comment

class PostViewSerializer(serializers.Serializer):

    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.CharField(source='user.username')

  