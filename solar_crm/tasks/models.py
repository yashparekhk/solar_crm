from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Task(models.Model):

    TYPE_CHOICES = [
        ('call',      'Call Reminder'),
        ('followup',  'Follow-up'),
        ('task',      'General Task'),
        ('meeting',   'Meeting'),
    ]
    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('in_progress', 'In Progress'),
        ('completed',   'Completed'),
        ('overdue',     'Overdue'),
    ]
    PRIORITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
    ]

    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    task_type    = models.CharField(max_length=20, choices=TYPE_CHOICES,     default='task')
    priority     = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES,   default='pending')

    assigned_to      = models.ForeignKey(User, on_delete=models.CASCADE,
                                         related_name='assigned_tasks')
    created_by       = models.ForeignKey(User, on_delete=models.CASCADE,
                                         related_name='created_tasks')

    # Optional links to existing CRM records
    related_lead     = models.ForeignKey('leads.Lead',         on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='tasks')
    related_customer = models.ForeignKey('customers.Customer', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='tasks')

    due_date     = models.DateField()
    due_time     = models.TimeField(null=True, blank=True)

    reminder_sent  = models.BooleanField(default=False)
    completed_at   = models.DateTimeField(null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', 'due_time']

    def __str__(self):
        return self.title

    def is_overdue(self):
        if self.status == 'completed':
            return False
        return self.due_date < timezone.now().date()

    def mark_overdue(self):
        """Auto-mark overdue tasks — called by management command."""
        if self.is_overdue() and self.status != 'overdue':
            self.status = 'overdue'
            self.save(update_fields=['status'])