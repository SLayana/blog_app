from rest_framework import serializers
from django.contrib.auth.models import User

from .models import UserProfile

class UserSerializer(serializers.Serializer):
    
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_id(self, obj):
        if isinstance(obj, User):
            return obj.id
        elif isinstance(obj, UserProfile):
            return obj.user_id
        
    def get_username(self, obj):
        if isinstance(obj, User):
            return obj.username
        elif isinstance(obj, UserProfile):
            return obj.user.username


class CreateUserSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    bio = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    birth_date = serializers.DateField()

    def create(self, obj):
        user = User.objects.create_user(username=obj['username'],
                                        password=obj['password'],
                                        email=obj['email'])
        UserProfile.objects.create(user=user, 
                                   bio=obj['bio'], 
                                   location=obj['location'], 
                                   birth_date=obj['birth_date'])
        return user



class UserDetailSerializer(UserSerializer):

    bio = serializers.CharField()
    location = serializers.CharField()
    birth_date = serializers.DateField()
    

