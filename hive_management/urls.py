from django.urls import path
from . import views

urlpatterns = [
    path('create-hive/', views.CreateHiveView.as_view(), name='create_hive'),
    path('edit-hive/<int:pk>/', views.EditHiveView.as_view(), name='edit_hive'),
    path('edit-state-hive/<int:pk>/', views.EditStateBeehiveView.as_view(), name = 'edit_state_hive'),
    path('detail-hive/<int:pk>/', views.DetailHiveView.as_view(), name='detail_hive'),
    path('detail-public-hive/<int:pk>/', views.DetailPublicHiveView.as_view(), name='detail_public_hive'),
    path('list-hives/', views.ListHivesView.as_view(), name='list_hives'),
    path('list-hives-admin/', views.ListHiveAdmin.as_view(), name='list-hives-admin')
    
]