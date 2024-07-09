from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserLoginSerializer, UserRegistrationSerializer, CustomUserSerializer, ProfileSerializer, ProfileAvatarSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from .models import Profile

class UserRegistrationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  # Calls the create method in UserRegistrationSerializer
                token = RefreshToken.for_user(user)
                data = serializer.data  # Serialized data
                print(serializer.data)
                print(f"User created: {user}, ID: {user.id}")
                data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
                return Response(data, status=status.HTTP_201_CREATED)
            return Response("Not valid data", status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            user_serializer = CustomUserSerializer(user)  # Serialize the authenticated user
            token = RefreshToken.for_user(user)
            data = user_serializer.data  # Serialized user data
            data["token"] = {"refresh": str(token), "access": str(token.access_token)}
            return Response(data, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class UserAPIView(GenericAPIView):
    """
    Get, Update user information
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer
    
    ## this function will return the currently authenticated user '(self.request.user)', which will be used by the the View to get 
    ## and update the user info
    def get_object(self):
        return self.request.user 
    
class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """
    
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    
    #Defining the queryset, so Generic View can use this to perform queries on Profile 
    queryset = Profile.objects.all()
    
    def get_object(self):
        return self.request.user.profile
    

class UserAvatarAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user avatar
    """
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileAvatarSerializer
    
    def get_object(self):
        return self.request.user.profile            
                            