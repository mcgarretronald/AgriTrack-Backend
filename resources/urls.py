from django.urls import path
from .views import ResourceListCreateView, ResourceDetailView

urlpatterns = [
    path("resources/", ResourceListCreateView.as_view(), name="resource-list-create"),
    path("resources/<str:resource_id>/", ResourceDetailView.as_view(), name="resource-detail"),  # ✅ Ensure this exists
]
