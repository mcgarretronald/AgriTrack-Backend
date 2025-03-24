from django.db import models
from crops.models import Crop
from activities.models import Activity
from resources.models import Resource
from users.models import User  # Importing the User model if it's in a separate file
import datetime

class Dashboard(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    
    total_crops = models.IntegerField(default=0)
    total_resources = models.IntegerField(default=0)
    upcoming_tasks = models.IntegerField(default=0)
    total_harvested = models.IntegerField(default=0)

    def __str__(self):
        return f"Dashboard for {self.user.username}"

    def update_dashboard(self, user_id):
        """
        Update the dashboard statistics for a specific user based on the user_id.
        """
        # Fetch the user instance using user_id
        user = User.objects.get(id=user_id)

        # Update the dashboard stats based on the data for the user
        self.total_crops = Crop.objects.filter(user=user).count()
        self.total_resources = Resource.objects.filter(user=user).count()
        
        # Count upcoming tasks: activities with a date greater than or equal to today
        self.upcoming_tasks = Activity.objects.filter(user=self.user, date__gte=datetime.date.today()).count()
        
        # Count crops that are ready for harvest
        self.total_harvested = Crop.objects.filter(user=user, status="Ready for Harvest").count()

        # Save the updated dashboard
        self.save()
