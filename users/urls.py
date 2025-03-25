from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register_permision/', views.canCreateView.as_view(), name='sign_up'),
    path('sign_up/', views.singUpView.as_view(), name='sign_up'),
    path('', views.loginView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
   