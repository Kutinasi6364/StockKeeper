from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.react_view, name='home'),
    path('home/', views.react_view, name='home'),
    path('home/api/', views.EquityHubHomeViewAPI.as_view(), name='home_api'),
    path('home/api/register/', views.EquityHubRegisterViewAPI.as_view(), name='register'),
    path('home/api/update/', views.EquityHubUpdateViewAPI.as_view(), name='update'),
    path('home/api/delete/<int:pk>/', views.EquityHubDeleteViewAPI.as_view(), name='delete'),
    path('analysis/', views.react_view, name='analysis'),
]
