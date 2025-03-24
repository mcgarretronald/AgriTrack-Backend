from rest_framework import serializers
from .models import Activity
from django.utils import timezone

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'description', 'date', 'user']  # Include all the necessary fields
        read_only_fields = ['id', 'user']  # user is set automatically from the request

    def validate_date(self, value):
        """
        Ensure the activity date is not in the past.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("Activity date cannot be in the past.")
        return value

    def validate_description(self, value):
        """
        Ensure the description is not empty or meaningless.
        """
        if not value or value.strip() == "":
            raise serializers.ValidationError("Description cannot be empty.")
        return value
