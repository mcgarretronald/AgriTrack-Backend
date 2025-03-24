import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse

def generate_unique_id():
    """Generate a unique 16-character alphanumeric ID."""
    return uuid.uuid4().hex[:16]

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('Seed', 'Seed'),
        ('Fertilizer', 'Fertilizer'),
        ('Pesticide', 'Pesticide'),
        ('Equipment', 'Equipment'),
        ('Other', 'Other'),
    ]

    USAGE_STATUS = [
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Depleted', 'Depleted'),
    ]

    MEASUREMENT_UNITS = [
        ('Bags', 'Bags'),
        ('Kilograms', 'Kilograms'),
        ('Liters', 'Liters'),
        ('Tons', 'Tons'),
        ('Units', 'Units'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources")
    resource_id = models.CharField(
        max_length=16,
        unique=True,
        default=generate_unique_id,
        editable=False
    )
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=20, choices=MEASUREMENT_UNITS, default='Units')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='Other')
    usage_status = models.CharField(max_length=20, choices=USAGE_STATUS, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_resource_name')
        ]

    def clean(self):
        if self.quantity < 0:
            raise ValidationError({'quantity': "Quantity cannot be negative."})

    def get_absolute_url(self):
        return reverse('user-resource-detail', kwargs={'user_id': self.user.id, 'resource_id': self.resource_id})

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.name} ({self.resource_type}) - {self.usage_status}"
