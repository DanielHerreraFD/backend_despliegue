from django.urls import path
from . import views

urlpatterns = [
    path('hive-harvesting/<int:pk>/', views.HiveHarvestingView.as_view(), name='hive_harvesting'),
    path('edit-hive-harvesting/<int:pk>/', views.EditHiveHarvestingView.as_view(), name='edit_hive_harvesting'),
    path('list-hive-harvesting/', views.ListHiveHarvestingView.as_view(), name='list_hive_harvesting'),
    path('list-public-hive-harvesting/', views.ListPublicHiveHarvestingView.as_view(), name='list_public_hive_harvesting'),
]