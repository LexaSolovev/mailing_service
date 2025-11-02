from django.urls import path
from . import views  # Убедитесь, что views.py существует

app_name = "clients"  # Пространство имён приложения

urlpatterns = [
    path("", views.ClientListView.as_view(), name="list"),
    path("create/", views.ClientCreateView.as_view(), name="create"),
    path("<int:pk>/", views.ClientDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.ClientUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.ClientDeleteView.as_view(), name="delete"),
]
