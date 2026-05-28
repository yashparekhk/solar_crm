from django.contrib import admin
from django.urls import path, include
from dashboard import views as dashboard_views
from tickets import views as ticket_views                  # ← ADDED

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
    path('tasks/',         include('tasks.urls')),
    path('site-survey/',   include('site_survey.urls')),
    path('',               include('accounts.urls')),

    # ── Public support page — no login needed ──
    path('support/', ticket_views.public_support_page, name='public_support_page'),  # ← ADDED

    path('api/dashboard-stats/',       dashboard_views.dashboard_stats_api,    name='dashboard_stats_api'),
    path('api/leads/<int:pk>/status/', dashboard_views.update_lead_status_api, name='update_lead_status_api'),
]