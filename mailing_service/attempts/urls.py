from django.urls import path
from . import views

app_name = "attempts"

urlpatterns = [
    path("", views.AttemptListView.as_view(), name="list"),
    path("<int:pk>/", views.AttemptDetailView.as_view(), name="detail"),
]
