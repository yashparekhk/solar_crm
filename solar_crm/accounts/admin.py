"""
Accounts admin configuration.
Naming Convention: PascalCase for admin classes
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin panel configuration for CustomUser model."""

    # Columns shown in list view — snake_case field names
    list_display   = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
    list_filter    = ['role', 'is_active', 'is_staff']
    search_fields  = ['username', 'first_name', 'last_name', 'email']
    ordering       = ['-date_joined']

    # Add custom fields to admin form
    fieldsets = UserAdmin.fieldsets + (
        ('Solar CRM Info', {
            'fields': ('role', 'phone', 'address')
        }),
    )