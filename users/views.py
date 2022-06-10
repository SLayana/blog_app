from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from blog_app.authentication import UserIsAuthOrReadOnly

from .serializers import UserSerializer, UserDetailSerializer, CreateUserSerializer, \
                         UpdateUserSerializer
from .models import UserProfile


class CreateOrListUserAPIView(APIView):

    authentication_classes = [UserIsAuthOrReadOnly]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response({
                    "status": "success",
                    "message": "",
                    "data": serializer.data
                })

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({
                    "status": "failure",
                    "message": "Request body has wrong data",
                    "data": serializer.errors
                }, status=400)
        return Response({
                    "status": "success",
                    "message": "User created successfully",
                    "data": None
                })

class UserDetailAPIView(APIView):

    authentication_classes = [UserIsAuthOrReadOnly]

    def get(self, request, id):
        try:
            user = UserProfile.objects.get(user_id=id)
        except UserProfile.DoesNotExist:
            return Response({
                    "status": "failure",
                    "message": "User does not exist",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDetailSerializer(user)
        return Response({
                    "status": "success",
                    "message": "",
                    "data": serializer.data
                })

    def post(self, request, id):
        try:
            User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({
                        "status": "failure",
                        "message": "User does not exist",
                        "data": None
                    }, status=status.HTTP_404_NOT_FOUND)

        try:
            user_profile = UserProfile.objects.get(user_id=id)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user_id=id)
        
        serializer = UpdateUserSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response({
                    "status": "success",
                    "message": "UserProfile updated successfully",
                    "data": None
                })
        else:
            return Response({
                    "status": "failure",
                    "message": "Request body has wrong data",
                    "data": serializer.errors
                }, status=400)

    def delete(self, request, id):

        try:
            User.objects.get(id=id).delete()
            return Response({
                        "status": "success",
                        "message": "User deleted successfully",
                        "data": None
                    })
        except User.DoesNotExist:
            return Response({
                        "status": "failure",
                        "message": "User does not exist",
                        "data": None
                    }, status=status.HTTP_404_NOT_FOUND)