from django.contrib import admin
from .models import Ticket, PublicTicket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display  = ['id', 'title', 'customer', 'priority', 'status', 'assigned_to', 'created_at']
    list_filter   = ['status', 'priority', 'category']
    search_fields = ['title', 'customer__name']
    ordering      = ['-created_at']


@admin.register(PublicTicket)
class PublicTicketAdmin(admin.ModelAdmin):
    list_display  = ['id', 'full_name', 'email', 'phone', 'category', 'subject', 'status', 'created_at']
    list_filter   = ['status', 'category']
    search_fields = ['full_name', 'email', 'phone', 'subject']
    ordering      = ['-created_at']