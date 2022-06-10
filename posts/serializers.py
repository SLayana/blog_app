from rest_framework import serializers

from .models import Post, Comment

class PostViewSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField()
    author = serializers.CharField(source='user.username')
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        serializers = CommentListSerializer(comments, many=True)
        return serializers.data

class CommentListSerializer(serializers.Serializer):

    id = serializers.CharField()
    comment = serializers.CharField()
    user = serializers.CharField(source='user.username')
