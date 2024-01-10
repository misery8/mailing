from django.urls import path

from .views import (
    ClientsListCreateAPIView,
    ClientUpdateAPIView,
)


urlpatterns = [
    path('clients/', ClientsListCreateAPIView.as_view()),
    path('clients/<int:pk>/', ClientUpdateAPIView.as_view()),
]
