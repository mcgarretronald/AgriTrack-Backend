from django.urls import path
from .views import CropListView, CropDetailView

urlpatterns = [
    path('crops/', CropListView.as_view(), name='crop-list'),
    path('crops/<str:pk>/', CropDetailView.as_view(), name='crop-detail'),
]
