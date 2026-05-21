from django.db import models
from customers.models import Customer

QUOTATION_STATUS_CHOICES = [
    ('draft',    'Draft'),
    ('sent',     'Sent'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class Quotation(models.Model):
    customer      = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Customer')
    quotation_no  = models.CharField(max_length=20, unique=True, verbose_name='Quotation Number')
    system_size   = models.DecimalField(max_digits=6,  decimal_places=2, verbose_name='System Size (kW)')
    total_amount  = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total Amount')
    status        = models.CharField(max_length=20, choices=QUOTATION_STATUS_CHOICES, default='draft')
    notes         = models.TextField(blank=True, verbose_name='Notes')
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quote #{self.quotation_no} — {self.customer.name}"

    class Meta:
        verbose_name        = 'Quotation'
        verbose_name_plural = 'Quotations'
        ordering            = ['-created_at']