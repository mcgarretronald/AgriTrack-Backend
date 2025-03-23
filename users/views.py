from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework.serializers import ValidationError
from .serializers import UserSerializer


User = get_user_model()


class RegisterUserView(generics.CreateAPIView):
    """User registration with improved error handling"""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            errors = e.detail  # Extract the validation errors

            # Custom error messages for email and username uniqueness
            formatted_errors = {}
            if "username" in errors:
                formatted_errors["error"] = "This username is already taken. Try a different one or log in."
            if "email" in errors:
                formatted_errors["error"] = "An account with this email already exists. Try logging in."

            return Response(formatted_errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response(
                {"error": "An account with this email or username already exists. Try logging in."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    """User login using email or username with password verification"""

    def post(self, request):
        identifier = request.data.get("identifier")  # Can be email or username
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"error": "Both identifier (email or username) and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find user by email or username
        user = User.objects.filter(email__iexact=identifier).first() if "@" in identifier else User.objects.filter(username__iexact=identifier).first()
        if not user:
            return Response({"error": "No account found with this email or username."}, status=status.HTTP_404_NOT_FOUND)

        # Authenticate user
        user = authenticate(email=user.email, password=password)
        if not user:
            return Response({"error": "Incorrect password. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"success": "Login successful", "user_id": user.id}, 
            status=status.HTTP_200_OK
        )

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve and update user profile by ID"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user_id = self.kwargs.get("id")  # Get ID from URL
        return get_object_or_404(User, id=user_id)

    def update(self, request, *args, **kwargs):
        # Restrict updating certain fields like `is_staff`
        protected_fields = ["is_staff", "is_superuser", "password"]
        for field in protected_fields:
            if field in request.data:
                return Response({"error": f"You cannot update the {field} field."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)
