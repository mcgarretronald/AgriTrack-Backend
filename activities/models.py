from django.db import models
from django.conf import settings
import uuid
from datetime import datetime
from django.utils import timezone

def generate_activity_id():
    return uuid.uuid4().hex[:16]

class Activity(models.Model):
    id = models.CharField(
        primary_key=True, max_length=16, unique=True, editable=False,
        default=generate_activity_id  # Use the function instead of the lambda
    )
    description = models.TextField()  # Add the description field
    date = models.DateField(default=timezone.now)  # Ensure default is callable
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)

    def save(self, *args, **kwargs):
        if isinstance(self.date, datetime):
            self.date = self.date.date()  # Ensure it's stored as a date
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Activity on {self.date}"

    class Meta:
        ordering = ["-date"]  # Show latest activities first
