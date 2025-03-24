from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Resource
from .serializers import ResourceSerializer

User = get_user_model()  # ✅ Get the user model


class ResourceListCreateView(generics.ListCreateAPIView):
    """Handles listing and creating resources"""
    serializer_class = ResourceSerializer

    def get_queryset(self):
        """Fetch only resources for the provided user_id"""
        user_id = self.request.query_params.get("user")  # ✅ Get user_id from query params
        if not user_id:
            return Resource.objects.none()  # ✅ Return an empty queryset if no user ID is provided

        return Resource.objects.filter(user_id=user_id)  # ✅ Fetch resources for the given user ID

    def perform_create(self, serializer):
        """Attach user before saving"""
        user = self.request.user if self.request.user.is_authenticated else None
        user_id = self.request.data.get("user")

        if not user_id and not user:
            raise ValidationError({"user": "User ID is required."})

        if not user:  # Fallback if no authentication system is used
            user = get_object_or_404(User, id=user_id)

        serializer.save(user=user)  # ✅ Attach user correctly


class ResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles retrieving, updating, and deleting resources"""
    serializer_class = ResourceSerializer
    lookup_field = "resource_id"  # ✅ Lookup based on `resource_id` instead of `pk`

    def get_object(self):
        """Fetch the requested resource and ensure it belongs to the provided user"""
        resource_id = self.kwargs.get("resource_id")  # ✅ Get `resource_id` from URL
        user_id = self.request.query_params.get("user")  # ✅ Optional user filter

        queryset = Resource.objects.all()
        resource = get_object_or_404(queryset, resource_id=resource_id)

        if user_id and str(resource.user.id) != str(user_id):
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

        return resource

    def update(self, request, *args, **kwargs):
        """Update a resource only if it belongs to the user"""
        instance = self.get_object()
        data = request.data.copy()

        # Prevent modification of `resource_id`
        if "resource_id" in data:
            data.pop("resource_id")

        serializer = self.get_serializer(instance, data=data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Delete a resource only if it belongs to the user"""
        instance = self.get_object()
        try:
            instance.delete()
            return Response({"message": "Resource deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": f"Failed to delete resource: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
