
import logging
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import RegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate



logger = logging.getLogger("my_project")


# class Registration(APIView):
#
#     def post(self, request):
#         logger.info("Received registration request")
#
#         try:
#             serializer = RegistrationSerializer(data=request.data)
#
#             if serializer.is_valid():
#                 user = serializer.save()
#                 logger.info(f"New user registered: {user.username} (Email: {user.email})")
#
#                 return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
#
#             logger.warning("Registration validation failed", extra={"errors": serializer.errors})
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         except Exception as e:
#             logger.critical(f"Unexpected error during registration: {str(e)}", exc_info=True)
#             return Response(
#                 {"error": "Something went wrong!", "details": "Please try again later."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer  # DRF optimized class

    def create(self, request, *args, **kwargs):
        logger.info("Incoming registration request")
        try:
            response = super().create(request, *args, **kwargs)
            username=response.data.get('username')
            message=f"User {username} registered successfully!"
            logger.info(f"{message}")
            return Response({"message": message},status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.critical(f"Registration failed: {str(e)}", exc_info=True)
            return Response(
                {"error": "Something went wrong!", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Login(GenericAPIView):
    serializer_class = LoginSerializer  # Automatic validation

    def post(self, request):

        try:
            serializer = self.get_serializer(data=request.data)
            print("DEBUG",serializer)
            if serializer.is_valid():
                user = serializer.validated_data["user"]  # User is already validated
                if user:
                    refresh = RefreshToken.for_user(user)
                    logger.info(f"User {user.username} logged in successfully.")
                    return Response(
                        {"message": "Login successful!", "access_token": str(refresh.access_token)},
                        status=status.HTTP_200_OK
                    )
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


        except Exception as e:
            logger.critical(f"Unexpected Error in LoginView: {str(e)}", exc_info=True)
            return Response(
                {"error": "Something went wrong!", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")