import jwt

from django.conf import settings
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import authentication
from rest_framework import exceptions

from django.contrib.auth.models import User


class UserAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        if request.token:
            try:
                token_payload = jwt.decode(request.token, settings.SECRET_KEY, algorithms=["HS256"])
            except:
                raise APIException({
                    "status": "error",
                    "message": "Invalid X-API-TOKEN",
                    "data": "null"
                })

            try:
                user = User.objects.get(id=token_payload['user_id'], is_active=True)
            except User.DoesNotExist:
                return Response({
                    "status": "failure",
                    "message": "User not found",
                    "data": None
                })
            
            request.user_id = user.id
        else:
            raise exceptions.AuthenticationFailed("No token")


class UserIsAuthOrReadOnly(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        if request.method in ['POST', 'DELETE'] and request.token:
            try:
                token_payload = jwt.decode(request.token, settings.SECRET_KEY, algorithms=["HS256"])
            except:
                raise APIException({
                    "status": "error",
                    "message": "Invalid X-API-TOKEN",
                    "data": "null"
                })

            try:
                user = User.objects.get(id=token_payload['user_id'], is_active=True)
            except User.DoesNotExist:
                return Response({
                    "status": "failure",
                    "message": "User not found",
                    "data": None
                })
            
            request.user_id = user.id

        elif request.method in ['GET']:
            pass
        else:
            raise exceptions.AuthenticationFailed("No token")