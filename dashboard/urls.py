from django.urls import path
from .views import DashboardStatsView

urlpatterns = [
    path('stats/<int:user_id>/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
