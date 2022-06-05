from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework_simplejwt.authentication import JWTAuthentication

from blog_app.authentication import UserAuthentication, UserIsAuthOrReadOnly
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, UserDetailSerializer, CreateUserSerializer
from .models import UserProfile


class CreateOrListUserAPIView(APIView):
    authentication_classes = [UserIsAuthOrReadOnly]
    # permission_classes = (IsAuthenticated,)

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
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)
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
            user_profile = UserProfile.objects.get(user_id=id)
        except UserProfile.DoesNotExist:
            return Response({
                    "status": "failure",
                    "message": "User does not exist",
                    "data": None
                }, status=status.HTTP_404_NOT_FOUND)

        user_profile.bio=request.data['bio']
        user_profile.location=request.data['location']
        user_profile.birth_date=request.data['birth_date']
        user_profile.save()

        return Response({
                    "status": "success",
                    "message": "UserProfile updated successfully",
                    "data": None
                })

    def delete(self, request, id):

        User.objects.get(id=id).delete()
        return Response({
                    "status": "success",
                    "message": "User deleted successfully",
                    "data": None
                })