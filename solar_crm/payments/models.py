from django.db import models
from customers.models import Customer

PAYMENT_STATUS_CHOICES = [
    ('paid',    'Paid'),
    ('unpaid',  'Unpaid'),
    ('partial', 'Partial'),
]

PAYMENT_METHOD_CHOICES = [
    ('cash',          'Cash'),
    ('bank_transfer', 'Bank Transfer'),
    ('upi',           'UPI'),
    ('cheque',        'Cheque'),
    ('card',          'Card'),
]

class Payment(models.Model):
    customer     = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount       = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Amount (₹)')
    status       = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_date = models.DateField(null=True, blank=True, verbose_name='Payment Date')
    method       = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, blank=True)
    notes        = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment ₹{self.amount} — {self.customer.name} ({self.get_status_display()})"

    class Meta:
        verbose_name        = 'Payment'
        verbose_name_plural = 'Payments'
        ordering            = ['-created_at']