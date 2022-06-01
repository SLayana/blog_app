from rest_framework.views import APIView
from rest_framework.response import Response

from blog_app.authentication import UserAuthentication

# Create your views here.
class ListUsers(APIView):
    authentication_classes = [UserAuthentication]

    def get(self, request):
        return Response({
                    "status": "success",
                    "message": "",
                    "data": None
                })