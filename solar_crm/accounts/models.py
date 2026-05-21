"""
Accounts models — Custom user model.
Naming Convention:
  - Class names: PascalCase
  - Field names: snake_case
  - Constants: SCREAMING_SNAKE_CASE
  - Methods: snake_case
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


# Role choices constant — SCREAMING_SNAKE_CASE
ROLE_CHOICES = [
    ('admin',    'Admin'),
    ('employee', 'Employee'),
    ('customer', 'Customer'),
]


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    PascalCase class name as per Python convention.
    """

    # snake_case field names
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone      = models.CharField(max_length=15, blank=True)
    address    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # snake_case method names
    def save(self, *args, **kwargs):
        """Override save to capitalize first/last name automatically."""
        if self.first_name:
            self.first_name = self.first_name.capitalize()
        if self.last_name:
            self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return full name with first and last name."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username

    def get_initials(self):
        """Return initials for avatar display."""
        first_initial = self.first_name[0].upper() if self.first_name else ''
        last_initial  = self.last_name[0].upper()  if self.last_name  else ''
        return f"{first_initial}{last_initial}" or self.username[0].upper()

    def is_admin_user(self):
        """Check if user has admin role."""
        return self.role == 'admin'

    def is_employee_user(self):
        """Check if user has employee role."""
        return self.role == 'employee'

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    class Meta:
        verbose_name      = 'User'
        verbose_name_plural = 'Users'
        ordering          = ['-created_at']