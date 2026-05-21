"""
Leads model.
Naming Convention:
  - Class: PascalCase
  - Fields: snake_case
  - Constants: SCREAMING_SNAKE_CASE
  - Methods: snake_case
"""

from django.db import models

# Status choices — SCREAMING_SNAKE_CASE constant
LEAD_STATUS_CHOICES = [
    ('new',       'New'),
    ('contacted', 'Contacted'),
    ('qualified', 'Qualified'),
    ('lost',      'Lost'),
]

# Lead source choices
LEAD_SOURCE_CHOICES = [
    ('website',      'Website'),
    ('referral',     'Referral'),
    ('social_media', 'Social Media'),
    ('cold_call',    'Cold Call'),
    ('exhibition',   'Exhibition'),
    ('other',        'Other'),
]


class Lead(models.Model):
    """
    Lead model — represents a potential solar customer.
    PascalCase class name, singular (not 'Leads').
    """

    # snake_case field names
    name       = models.CharField(max_length=100, verbose_name='Full Name')
    phone      = models.CharField(max_length=15,  verbose_name='Phone Number')
    email      = models.EmailField(blank=True,     verbose_name='Email Address')
    address    = models.TextField(blank=True,      verbose_name='Address')
    source     = models.CharField(
        max_length=50,
        choices=LEAD_SOURCE_CHOICES,
        blank=True,
        verbose_name='Lead Source'
    )
    status     = models.CharField(
        max_length=20,
        choices=LEAD_STATUS_CHOICES,
        default='new',
        verbose_name='Status'
    )
    notes      = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True,     verbose_name='Updated At')

    def save(self, *args, **kwargs):
        """Auto capitalize name before saving."""
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    def is_qualified(self):
        """Check if lead is qualified."""
        return self.status == 'qualified'

    def is_new_lead(self):
        """Check if lead is new."""
        return self.status == 'new'

    def __str__(self):
        return f"{self.name} — {self.get_status_display()}"

    class Meta:
        verbose_name        = 'Lead'
        verbose_name_plural = 'Leads'
        ordering            = ['-created_at']