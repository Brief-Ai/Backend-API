from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserLoginSerializer, UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TokenSerializer



# Max
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException

class CustomAPIException(APIException):
    status_code = 400
    default_detail = "Bad Request"
    default_code = "bad_request"


@api_view(['POST',])
def logout_user(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST',])
def user_register_view(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Account has been created successfully!'
            data['username'] = account.username
            
            token = Token.objects.get(user=account).key
            data['token'] = token
            
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['POST'])
def login_user(request):
    if request.method == "POST":
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token) 
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def validate_token(request):
#     access_token = request.data.get('token')
#     print('Checking token +++++ ', access_token)

#     if access_token:
#         try:
#             token = AccessToken(access_token)
#             # Debug
#             print('Token is valid: ', token)
#             if token.check_blacklist():  # Check if the token is blacklisted (revoked)
#                 return Response({"status": "Invalid token 1"}, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             return Response({"status": "Invalid token 2"}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response({"status": "OK"}, status=status.HTTP_200_OK)
#     else:
#         return Response({"status": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_token(request):    
    # Debug, print user
    print('Validated Token For User User: ', request.user.username, ' User ID: ', request.user.id)
    return Response({"status": "OK"}, status=status.HTTP_200_OK)

# Make method to regenerate access token from refresh token
@api_view(['POST'])
def refresh_token(request):
    if request.method == "POST":
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            refresh = RefreshToken(token)
            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)