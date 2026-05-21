"""
Leads admin configuration.
"""

from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Admin configuration for Lead model."""

    list_display   = ['name', 'phone', 'email', 'source', 'status', 'created_at']
    list_filter    = ['status', 'source']
    search_fields  = ['name', 'phone', 'email']
    ordering       = ['-created_at']
    list_per_page  = 25