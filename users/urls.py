from django.urls import path

from users.views import CreateOrListUserAPIView, UserDetailAPIView

urlpatterns = [
    
    path('users', CreateOrListUserAPIView.as_view(), name='list_users'),
    path('users/<int:id>', UserDetailAPIView.as_view(), name='user_detail'),
   
]