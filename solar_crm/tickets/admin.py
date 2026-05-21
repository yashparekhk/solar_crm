from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'customer', 'priority', 'status', 'assigned_to', 'created_at']
    list_filter   = ['status', 'priority', 'category']
    search_fields = ['title', 'customer__name']
    ordering      = ['-created_at']