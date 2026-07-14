from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('result/<int:pk>/', views.result_detail, name='result_detail'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('history/delete/<int:pk>/', views.delete_prediction, name='delete_prediction'),
    path('history/export/', views.export_history_csv, name='export_history_csv'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('admin-retrain/', views.admin_retrain, name='admin_retrain'),
]
