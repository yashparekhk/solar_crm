from django.db import models
from customers.models import Customer

INSTALLATION_STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('progress',  'In Progress'),
    ('completed', 'Completed'),
    ('on_hold',   'On Hold'),
]

class Installation(models.Model):
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE)
    system_size = models.DecimalField(max_digits=6, decimal_places=2)
    start_date  = models.DateField(verbose_name='Start Date')
    end_date    = models.DateField(null=True, blank=True, verbose_name='End Date')
    status      = models.CharField(max_length=20, choices=INSTALLATION_STATUS_CHOICES, default='scheduled')
    technician  = models.CharField(max_length=100, blank=True, verbose_name='Technician Name')
    notes       = models.TextField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Installation — {self.customer.name} ({self.get_status_display()})"

    class Meta:
        verbose_name        = 'Installation'
        verbose_name_plural = 'Installations'
        ordering            = ['-created_at']