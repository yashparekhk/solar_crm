from django.contrib import admin
from .models import Installation

@admin.register(Installation)
class InstallationAdmin(admin.ModelAdmin):
    list_display  = ['customer', 'system_size', 'technician', 'status', 'start_date']
    list_filter   = ['status']
    search_fields = ['customer__name', 'technician']
    ordering      = ['-created_at']