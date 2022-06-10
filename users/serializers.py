from datetime import date
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


class UpdateUserSerializer(serializers.Serializer):

    bio = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    birth_date = serializers.DateField()

    def validate(self, data):
        today = date.today()
        birth_date = data.get('birth_date')
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 15:
            raise serializers.ValidationError("User is underage")
        return data

    def update(self, instance, validated_data):
        instance.bio=validated_data['bio']
        instance.location=validated_data['location']
        instance.birth_date=validated_data['birth_date']
        instance.save()
        return instance


class CreateUserSerializer(UpdateUserSerializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    

    def validate(self, data):
        super().validate(data)
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError("Provided username already exist")
        return data

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
    

