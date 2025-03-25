from django.urls import path
from . import views

urlpatterns = [
    path('create-beekeeper/', views.createBeekeeperView.as_view(), name='create_beekeeper'),
    path('edit-state-beekeeper/<int:pk>/', views.editStateBeekeeperView.as_view(), name = 'edit_state_beekeeper'),
    path('edit-beekeeper/<int:pk>/', views.editBeekeeperView.as_view(), name='edit_beekeeper'),
    path('detail-beekeeper/<int:pk>/', views.detailBeekeeperView.as_view(), name='detail_beekeeper'),
    path('list-beekeepers/', views.listBeekeepersView.as_view(), name='list_beekeepers'),
]