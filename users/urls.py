from django.urls import path

from users.views import ListUsers

urlpatterns = [
    
    path('users', ListUsers.as_view(), name='list_users'),
]