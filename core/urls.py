from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('payment/', views.payment_page, name='payment_page'),
    path('charge/', views.charge, name='charge'),
    path('invoice/', views.generate_invoice, name='invoice'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('repair-companies/', views.repair_companies, name='repair_companies'),
    path('repair-companies/<int:company_id>/services/', views.company_services, name='company_services'),
    path('compare-services/', views.compare_services, name='compare_services'),
    path('analytics/', views.analytics, name='analytics'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'), 
    path('mock-analytics/', views.mock_analytics, name='mock_analytics'),
    path("predict-service/", views.predict_service, name="predict_service"),
    path('documentation/', views.documentation, name='documentation'),
]
