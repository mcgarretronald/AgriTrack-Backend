from django.conf import settings
from django.db import models

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('seed', 'Seed'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('equipment', 'Equipment'),
    ]

    USAGE_STATUS = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('depleted', 'Depleted'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    quantity = models.PositiveIntegerField()
    usage_status = models.CharField(max_length=50, choices=USAGE_STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.quantity} units"