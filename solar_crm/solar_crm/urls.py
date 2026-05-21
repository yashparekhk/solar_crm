from django.contrib import admin
from django.urls import path, include

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
]