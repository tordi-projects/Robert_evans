from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/<int:pk>/', views.admin_conversation, name='admin_conversation'),
]
