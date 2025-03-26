from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Dashboard
from users.models import User

class DashboardStatsView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=str(user_id))
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        dashboard, created = Dashboard.objects.get_or_create(user=user)
        dashboard.update_dashboard(user_id=str(user_id))
        data = {
            "total_crops": dashboard.total_crops,
            "total_resources": dashboard.total_resources,
            "upcoming_tasks": dashboard.upcoming_tasks,
            "total_harvested": dashboard.total_harvested,
        }
        return Response(data)
