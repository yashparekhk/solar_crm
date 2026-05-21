"""
Customers model.
"""

from django.db import models


class Customer(models.Model):
    """Customer model — represents a confirmed solar customer."""

    name        = models.CharField(max_length=100, verbose_name='Full Name')
    phone       = models.CharField(max_length=15,  verbose_name='Phone Number')
    email       = models.EmailField(blank=True,     verbose_name='Email Address')
    address     = models.TextField(verbose_name='Address')
    city        = models.CharField(max_length=50,  verbose_name='City')
    system_size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='System Size (kW)'
    )
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at  = models.DateTimeField(auto_now=True,     verbose_name='Updated At')

    def save(self, *args, **kwargs):
        """Auto capitalize name and city."""
        if self.name: self.name = self.name.title()
        if self.city: self.city = self.city.title()
        super().save(*args, **kwargs)

    def get_system_size_display_text(self):
        """Return formatted system size."""
        return f"{self.system_size} kW"

    def __str__(self):
        return f"{self.name} — {self.city}"

    class Meta:
        verbose_name        = 'Customer'
        verbose_name_plural = 'Customers'
        ordering            = ['-created_at']