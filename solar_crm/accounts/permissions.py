"""
Permission helpers for Solar CRM role-based access control.

Roles:
  admin    — Full access to everything
  employee — Limited access based on assignments
  customer — View only their own profile
"""

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    """Only admin can access this view."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_view')
        if request.user.role != 'admin':
            messages.error(
                request,
                'Access denied. This action requires admin privileges.'
            )
            return redirect('dashboard_view')
        return view_func(request, *args, **kwargs)
    return wrapper


def employee_or_admin_required(view_func):
    """Admin and employee can access this view."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_view')
        if request.user.role not in ['admin', 'employee']:
            messages.error(
                request,
                'Access denied. You do not have permission to view this page.'
            )
            return redirect('dashboard_view')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_user_permissions(user):
    """
    Returns a dict of what the user can do.
    Used in templates via context.
    """
    is_admin    = user.role == 'admin'
    is_employee = user.role == 'employee'
    is_customer = user.role == 'customer'

    return {
        # Leads
        'can_create_lead':    is_admin,
        'can_delete_lead':    is_admin,
        'can_assign_lead':    is_admin,
        'can_view_all_leads': is_admin,
        'can_edit_lead':      is_admin or is_employee,

        # Customers
        'can_create_customer': is_admin,
        'can_delete_customer': is_admin,
        'can_edit_customer':   is_admin or is_employee,
        'can_view_customer':   is_admin or is_employee,

        # Quotations
        'can_create_quotation': is_admin or is_employee,
        'can_delete_quotation': is_admin,
        'can_edit_quotation':   is_admin or is_employee,

        # Installations
        'can_create_installation': is_admin or is_employee,
        'can_delete_installation': is_admin,
        'can_edit_installation':   is_admin or is_employee,

        # Payments
        'can_create_payment': is_admin,
        'can_delete_payment': is_admin,
        'can_edit_payment':   is_admin,
        'can_view_payment':   is_admin or is_employee,

        # Tickets
        'can_create_ticket': is_admin or is_employee,
        'can_delete_ticket': is_admin,
        'can_edit_ticket':   is_admin or is_employee,

        # Users
        'can_manage_users': is_admin,

        # Export/Import
        'can_export': is_admin or is_employee,
        'can_import': is_admin,

        # Role flags
        'is_admin':    is_admin,
        'is_employee': is_employee,
        'is_customer': is_customer,
    }