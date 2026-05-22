from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views

urlpatterns = [
    path('admin/',         admin.site.urls),
    path('accounts/',      include('accounts.urls')),
    path('dashboard/',     include('dashboard.urls')),
    path('leads/',         include('leads.urls')),
    path('customers/',     include('customers.urls')),
    path('quotations/',    include('quotations.urls')),
    path('installations/', include('installations.urls')),
    path('payments/',      include('payments.urls')),
    path('tickets/',       include('tickets.urls')),
    path('',               include('accounts.urls')),
    path('api/dashboard-stats/',       dashboard_views.dashboard_stats_api,    name='dashboard_stats_api'),
    path('api/leads/<int:pk>/status/', dashboard_views.update_lead_status_api, name='update_lead_status_api'),
]