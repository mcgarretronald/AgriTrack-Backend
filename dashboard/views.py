from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Dashboard
from rest_framework.permissions import IsAuthenticated

class DashboardStatsView(APIView):
    

    def get(self, request, user_id):
        """
        Endpoint to retrieve and update the dashboard for a specific user.
        """
        # Retrieve the user's dashboard, or create it if it doesn't exist
        dashboard, created = Dashboard.objects.get_or_create(user_id=user_id)

        # Update the dashboard for the specific user
        dashboard.update_dashboard(user_id=user_id)

        # Return the updated dashboard data
        data = {
            "total_crops": dashboard.total_crops,
            "total_resources": dashboard.total_resources,
            "upcoming_tasks": dashboard.upcoming_tasks,
            "total_harvested": dashboard.total_harvested,
        }

        return Response(data)
