from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ClientViewSet,
    MailingViewSet,
    NotificationStatisticsViewSet,
    NotificationCreateAPIView
)

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('mailings', MailingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('mailings/<int:pk>/statistics/', NotificationStatisticsViewSet.as_view()),
    path('mailings/statistics/', NotificationStatisticsViewSet.as_view()),
    path('notifications/', NotificationCreateAPIView.as_view())
]
