from django.db import models
from django.conf import settings  # To refer to the custom User model
import uuid


class Crop(models.Model):
    STATUS_CHOICES = [
        ('Planting', 'Planting'),
        ('Growing', 'Growing'),
        ('Harvesting', 'Harvesting'),
    ]

    id = models.CharField(primary_key=True, max_length=16, editable=False)  # Custom ID field
    name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100)
    planting_date = models.DateField()
    harvest_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    
    # Reference to the user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Function to generate a custom ID for the crop
    def generate_id(self):
        return str(uuid.uuid4().int)[:16]  # Generate a UUID and take the first 16 digits as a string

    def save(self, *args, **kwargs):
        if not self.id:  # Only set the ID if it's a new object
            self.id = self.generate_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.variety}"

    class Meta:
        ordering = ['-planting_date']  # Order crops by planting_date (newest first)