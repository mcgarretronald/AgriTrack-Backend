from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, NotFound

# Get the User model
User = get_user_model()

def get_user_from_request(request, from_query_params=False):
    """
    Helper method to fetch the user based on user_id from request.
    Allows retrieving user_id from either request data or query parameters.
    """
    user_id = request.query_params.get('user_id') if from_query_params else request.data.get('user_id')
    if not user_id:
        raise ValidationError({"detail": "User ID is backend required"})

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFound({"detail": "User not found"})


class ActivityListView(generics.ListCreateAPIView):
    """
    List all activities for the user or create a new activity.
    """
    serializer_class = ActivitySerializer

    def get_queryset(self):
        """
        Return a list of activities for the user specified in the query parameter.
        """
        user = get_user_from_request(self.request, from_query_params=True)
        return Activity.objects.filter(user=user).order_by('-date')  # Latest first

    def perform_create(self, serializer):
        """
        Set the user to the provided user_id before saving the activity.
        """
        user = get_user_from_request(self.request)
        serializer.save(user=user)  # Save the activity with the user


class ActivityDetailView(APIView):
    """
    Retrieve, update, or delete a specific activity.
    """

    def get(self, request, pk):
        """
        Retrieve a specific activity.
        """
        try:
            activity = Activity.objects.get(id=pk)  # Find activity by id
        except Activity.DoesNotExist:
            raise NotFound({"detail": "Activity not found"})
        
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Delete a specific activity.
        """
        try:
            activity = Activity.objects.get(id=pk)  # Find activity by id (no user check)
        except Activity.DoesNotExist:
            raise NotFound({"detail": "Activity not found"})
        
        activity.delete()  # Delete the activity
        return Response(status=status.HTTP_204_NO_CONTENT)
