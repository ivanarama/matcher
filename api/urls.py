from django.urls import path
from .views import match_view

urlpatterns = [
    path("match/", match_view),
]