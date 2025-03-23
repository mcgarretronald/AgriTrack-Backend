from rest_framework import serializers
from .models import Crop
from django.utils import timezone
from datetime import datetime


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['id', 'name', 'variety', 'planting_date', 'harvest_date', 'status', 'user']
        read_only_fields = ['id', 'user']  # user is set automatically from the request

    def validate_planting_date(self, value):
        """
        Ensure planting_date is not in the past.
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("Planting date cannot be in the past.")
        return value

    def validate_harvest_date(self, value):
        """
        Ensure harvest_date is after planting_date.
        """
        planting_date = self.initial_data.get('planting_date')
        if planting_date:
            # If planting_date is a string, convert it to a datetime.date object
            if isinstance(planting_date, str):
                planting_date = datetime.strptime(planting_date, "%Y-%m-%d").date()
            if value < planting_date:
                raise serializers.ValidationError("Harvest date must be after planting date.")
        return value

    def validate_status(self, value):
        """
        Ensure status is one of the allowed values.
        """
        allowed_statuses = ['Planting', 'Growing', 'Harvesting']
        if value not in allowed_statuses:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(allowed_statuses)}")
        return value