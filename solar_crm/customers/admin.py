from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display  = ['name', 'phone', 'city', 'system_size', 'created_at']
    list_filter   = ['city']
    search_fields = ['name', 'phone', 'email', 'city']
    ordering      = ['-created_at']