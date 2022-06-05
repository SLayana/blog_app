from django.urls import path

from .views import CreateOrListPostAPIView, PostAPIView

urlpatterns = [
    
    path('posts', CreateOrListPostAPIView.as_view(), name='create_post'),
    path('posts/<int:id>', PostAPIView.as_view(), name='modify_post')
    
]