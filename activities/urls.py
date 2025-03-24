from django.urls import path
from . import views

urlpatterns = [
    # Activity URLs
    path('activities/', views.ActivityListView.as_view(), name='activity-list-create'),
    path('activities/<str:pk>/', views.ActivityDetailView.as_view(), name='activity-detail'),

]
