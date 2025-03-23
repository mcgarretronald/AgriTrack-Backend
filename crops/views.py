from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import generics
from .models import Crop
from .serializers import CropSerializer
from django.contrib.auth import get_user_model

# Get the User model
User = get_user_model()


def get_user_from_request(request, from_query_params=False):
    """
    Helper method to fetch the user based on user_id from request.
    """
    user_id = request.query_params.get('user_id') if from_query_params else request.data.get('user_id')
    if not user_id:
        raise ValidationError({"detail": "User ID is required"})

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound({"detail": "User not found"})


def get_crop_for_user(user, crop_id):
    """
    Helper method to fetch a crop and ensure it belongs to the user.
    """
    try:
        return Crop.objects.get(pk=crop_id, user=user)
    except Crop.DoesNotExist:
        raise NotFound({"detail": "Crop not found or doesn't belong to the user"})
    
    
class CropListView(generics.ListCreateAPIView):
    serializer_class = CropSerializer
    

    def get_queryset(self):
        """
        Return a list of crops for the user specified in the query parameter.
        """
        user = get_user_from_request(self.request, from_query_params=True)
        return Crop.objects.filter(user=user).order_by('-planting_date')  # Latest first

    def perform_create(self, serializer):
        """
        Set the user to the provided user_id before saving the crop.
        """
        user = get_user_from_request(self.request)
        serializer.save(user=user)  # Save the crop with the user
        
class CropDetailView(APIView):
    

    def get(self, request, pk):
        """
        Retrieve a specific crop.
        """
        user = get_user_from_request(request, from_query_params=True)
        crop = get_crop_for_user(user, pk)
        serializer = CropSerializer(crop)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific crop.
        """
        user = get_user_from_request(request)
        crop = get_crop_for_user(user, pk)

        serializer = CropSerializer(crop, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the updated crop
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific crop.
        """
        user = get_user_from_request(request, from_query_params=True)
        crop = get_crop_for_user(user, pk)

        crop.delete()  # Delete the crop
        return Response(status=status.HTTP_204_NO_CONTENT)