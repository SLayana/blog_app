from django.urls import path

from .views import CreateOrListPostAPIView, PostAPIView, AddPostCommentAPIView, UpdateDeleteCommentAPIView

urlpatterns = [
    
    path('posts', CreateOrListPostAPIView.as_view(), name='create_post'),
    path('posts/<int:post_id>', PostAPIView.as_view(), name='modify_post'),
    path('posts/<int:post_id>/comments', AddPostCommentAPIView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>', UpdateDeleteCommentAPIView.as_view(), name='modify_comment'),
   
]