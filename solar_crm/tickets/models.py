from django.db import models
from customers.models import Customer
from accounts.models import CustomUser

TICKET_STATUS_CHOICES = [
    ('open',        'Open'),
    ('in_progress', 'In Progress'),
    ('resolved',    'Resolved'),
    ('closed',      'Closed'),
]

TICKET_PRIORITY_CHOICES = [
    ('low',    'Low'),
    ('medium', 'Medium'),
    ('high',   'High'),
    ('urgent', 'Urgent'),
]

TICKET_CATEGORY_CHOICES = [
    ('installation', 'Installation Issue'),
    ('billing',      'Billing Issue'),
    ('technical',    'Technical Support'),
    ('general',      'General Inquiry'),
    ('complaint',    'Complaint'),
    ('other',        'Other'),
]


class Ticket(models.Model):
    title       = models.CharField(max_length=200, verbose_name='Title')
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Customer')
    category    = models.CharField(max_length=50, choices=TICKET_CATEGORY_CHOICES, default='general')
    priority    = models.CharField(max_length=20, choices=TICKET_PRIORITY_CHOICES, default='medium')
    status      = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='open')
    description = models.TextField(verbose_name='Description')
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Assigned To'
    )
    notes      = models.TextField(blank=True, verbose_name='Internal Notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.pk} — {self.title} ({self.get_status_display()})"

    class Meta:
        verbose_name        = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering            = ['-created_at']


class PublicTicket(models.Model):
    full_name  = models.CharField(max_length=150, verbose_name='Full Name')
    email      = models.EmailField(verbose_name='Email Address')
    phone      = models.CharField(max_length=20, verbose_name='Phone Number')
    category   = models.CharField(max_length=50, choices=TICKET_CATEGORY_CHOICES, default='general', verbose_name='Category')
    subject    = models.CharField(max_length=200, verbose_name='Subject')
    message    = models.TextField(verbose_name='Message')
    status     = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.pk} — {self.subject} ({self.full_name})"

    class Meta:
        verbose_name        = 'Public Ticket'
        verbose_name_plural = 'Public Tickets'
        ordering            = ['-created_at']