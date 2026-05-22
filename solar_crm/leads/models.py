from django.db import models
from django.conf import settings

LEAD_STATUS_CHOICES = [
    ('new',       'New'),
    ('contacted', 'Contacted'),
    ('qualified', 'Qualified'),
    ('lost',      'Lost'),
]

LEAD_SOURCE_CHOICES = [
    ('website',      'Website'),
    ('referral',     'Referral'),
    ('social_media', 'Social Media'),
    ('cold_call',    'Cold Call'),
    ('exhibition',   'Exhibition'),
    ('other',        'Other'),
]


class Lead(models.Model):
    name        = models.CharField(max_length=100, verbose_name='Full Name')
    phone       = models.CharField(max_length=15,  verbose_name='Phone Number')
    email       = models.EmailField(blank=True,     verbose_name='Email Address')
    address     = models.TextField(blank=True,      verbose_name='Address')
    source      = models.CharField(max_length=50, choices=LEAD_SOURCE_CHOICES, blank=True)
    status      = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    notes       = models.TextField(blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete    = models.SET_NULL,
        null         = True,
        blank        = True,
        related_name = 'assigned_leads',
        verbose_name = 'Assigned To',
        limit_choices_to = {'role__in': ['admin', 'employee']},
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    def is_assigned_to(self, user):
        return self.assigned_to == user

    def can_edit(self, user):
        if user.role == 'admin':
            return True
        if user.role == 'employee' and self.assigned_to == user:
            return True
        return False

    def __str__(self):
        return f"{self.name} — {self.get_status_display()}"

    class Meta:
        verbose_name        = 'Lead'
        verbose_name_plural = 'Leads'
        ordering            = ['-created_at']