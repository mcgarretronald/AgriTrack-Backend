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
        email = request.data.get("email")
        username = request.data.get("username")

        # Explicitly check for existing email and username
        if User.objects.filter(email=email).exists():
            return Response({"error": "An account with this email already exists. Try logging in."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "This username is already taken. Try a different one or log in."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(
                {"error": "An account with this email or username already exists. Try logging in."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LoginUserView(APIView):
    """User login using either email or username with password verification"""

    def post(self, request):
        identifier = request.data.get("identifier")  # Can be email or username
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"error": "Both identifier (email or username) and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find the user by email or username
        user = User.objects.filter(email__iexact=identifier).first() or \
               User.objects.filter(username__iexact=identifier).first()

        if not user:
            return Response({"error": "No account found with this email or username."}, status=status.HTTP_404_NOT_FOUND)

        # Authenticate using email (since email is the USERNAME_FIELD)
        user = authenticate(request, username=user.email, password=password)  # 🔹 Fix: Use `email`
        if not user:
            return Response({"error": "Incorrect password. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"success": "Login successful", "user_id": user.id, "username": user.username, "email": user.email}, 
            status=status.HTTP_200_OK
        )

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve and update user profile by ID"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Get user profile based on the provided ID"""
        user_id = self.kwargs.get("id")
        return get_object_or_404(User, id=user_id)

    def update(self, request, *args, **kwargs):
        """Restrict updates to protected fields and ensure valid data"""
        protected_fields = {"is_staff", "is_superuser", "password"}
        data = request.data.copy()

        # Remove protected fields from request data
        for field in protected_fields:
            if field in data:
                return Response({"error": f"Updating {field} is not allowed."}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object()

        serializer = self.get_serializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)