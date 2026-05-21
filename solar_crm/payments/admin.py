from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['customer', 'amount', 'status', 'method', 'payment_date', 'created_at']
    list_filter   = ['status', 'method']
    search_fields = ['customer__name']
    ordering      = ['-created_at']