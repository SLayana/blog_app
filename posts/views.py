from ast import Delete
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from blog_app.authentication import UserAuthentication, UserIsAuthOrReadOnly
from .models import Post, Comment
from .serializers import PostViewSerializer


class CreateOrListPostAPIView(APIView):

    authentication_classes = [UserIsAuthOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostViewSerializer(posts, many=True)
        return Response({
                    "status": "success",
                    "message": "",
                    "data": serializer.data
                })

    def post(self, request):
        user_id = request.user_id
        title = request.data['title']
        content = request.data['content']
        Post.objects.create(user_id=user_id, title=title, content=content)

        return Response({
                    "status": "success",
                    "message": "Post created successfully",
                    "data": None
                })


class PostAPIView(APIView):

    authentication_classes = [UserIsAuthOrReadOnly]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({
                    "status": "failure",
                    "message": "Post does not exist",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)

        serializer = PostViewSerializer(post)
        return Response({
                    "status": "success",
                    "message": "",
                    "data": serializer.data,
                })
    
    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, user_id=request.user_id)
        except Post.DoesNotExist:
            return Response({
                    "status": "failure",
                    "message": "Post does not exist or you are not the author of the post",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)

        post.title = request.data['title']
        post.content = request.data['content']
        post.save()
        return Response({
                    "status": "success",
                    "message": "Post updated successfully",
                    "data": None
                })

    def delete(self, request, post_id):
        try:
            Post.objects.get(id=post_id, user_id=request.user_id).delete()
        except Post.DoesNotExist:
            return Response({
                    "status": "failure",
                    "message": "Post does not exist or you are not the author of the post",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
                    "status": "success",
                    "message": "Post deleted successfully",
                    "data": None
                })


class AddPostCommentAPIView(APIView):

    authentication_classes = [UserIsAuthOrReadOnly]

    def post(self, request, post_id):
        Comment.objects.create(post_id=post_id, 
                               comment=request.data['comment'], 
                               user_id=request.user_id)
        
        return Response({
                    "status": "success",
                    "message": "Comment created successfully",
                    "data": None
                })
        

class UpdateDeleteCommentAPIView(APIView):

    authentication_classes = [UserIsAuthOrReadOnly]

    def post(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({
                    "status": "failure",
                    "message": "Comment does not exist",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)

        comment.comment = request.data['comment']
        comment.save()
        return Response({
                    "status": "success",
                    "message": "Comment updated successfully",
                    "data": None
                })

    def delete(self, request, post_id, comment_id):
        try:
            Comment.objects.get(id=comment_id).delete()
        except Comment.DoesNotExist:
            return Response({
                    "status": "failure",
                    "message": "Comment does not exist",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
                    "status": "success",
                    "message": "Comment deleted successfully",
                    "data": None
                })

