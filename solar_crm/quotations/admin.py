from django.contrib import admin
from .models import Quotation

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display  = ['quotation_no', 'customer', 'system_size', 'total_amount', 'status']
    list_filter   = ['status']
    search_fields = ['quotation_no', 'customer__name']
    ordering      = ['-created_at']