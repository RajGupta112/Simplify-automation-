from django.urls import path

from .views import LeadCreateAPIView


urlpatterns = [
    path(
        "submit/",
        LeadCreateAPIView.as_view(),
        name="lead-submit",
    ),
]