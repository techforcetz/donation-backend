from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import Register_Serializer,Login_Serializer
from django.contrib.auth import login,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

# Create your views here.
class Register(CreateAPIView):
    serializer_class = Register_Serializer

    def post(self,request):
        serializer = Register_Serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created successfuly"},status=201)
        print(f"registering user {request.data}")
        return Response({"Error":serializer.error_messages},status=401)

class Login(APIView):
    def post(self,request):
        serializer = Login_Serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "message":f"welcome {user.username}",
                "access":str(refresh.access_token),
                "refresh":str(refresh)
            },status=201)
        return Response({"error":"unable to login"},status=401)

class Logout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Invalidate the refresh token
                
            # Optionally clear access token from client side
            return Response(
                {"message": "Successfully logged out"}, 
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
