from django.urls import path
from . import views

urlpatterns = [
    path('beehive-monitoring/<int:pk>/', views.BeehiveMonitoringView.as_view(), name='beehive_monitoring'),
    path('edit-beehive-monitoring/<int:pk>/', views.EditBeehiveMonitoringView.as_view(), name='edit_beehive_monitoring'),
    path('list-beehive-monitoring/', views.ListBeehiveMonitoringView.as_view(), name='list_beehive_monitoring'),
]