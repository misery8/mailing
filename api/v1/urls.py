from django.urls import path

from .views import (
    ClientCreateAPIView,
    ClientAPIView,
    MailingStatisticListAPIView,
    MailingStatisticDetailAPIView,
    MailingAPIView,
)


urlpatterns = [
    path('clients/', ClientCreateAPIView.as_view()),
    path('clients/<int:pk>/', ClientAPIView.as_view()),
    path('mailing/statistic/', MailingStatisticListAPIView.as_view()),
    path('mailing/<int:pk>/statistic/', MailingStatisticDetailAPIView.as_view()),
    path('mailing/<int:pk>/', MailingAPIView.as_view()),
]
