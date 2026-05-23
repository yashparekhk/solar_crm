"""
Dashboard views.
Naming Convention:
  - Function names: snake_case ending with '_view'
  - Variables: snake_case
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
import json


@login_required(login_url='/accounts/login/')
def dashboard_view(request):
    """Main dashboard view showing all CRM statistics."""

    # Default context values — snake_case keys
    dashboard_context = {
        'total_leads':         0,
        'total_customers':     0,
        'total_quotations':    0,
        'total_installations': 0,
        'pending_payments':    0,
        'total_revenue':       0,
        'recent_leads':        [],
        'recent_customers':    [],
        'page_title':          'Dashboard',
        'leads_new':           0,
        'leads_contacted':     0,
        'leads_qualified':     0,
        'leads_proposal':      0,
        'leads_won':           0,
        'task_today':          0,
        'task_overdue':        0,
    }

    # Import models safely
    try:
        from leads.models import Lead
        from customers.models import Customer
        from quotations.models import Quotation
        from installations.models import Installation
        from payments.models import Payment

        # Count stats
        total_leads         = Lead.objects.count()
        total_customers     = Customer.objects.count()
        total_quotations    = Quotation.objects.count()
        total_installations = Installation.objects.count()
        pending_payments    = Payment.objects.filter(status='unpaid').count()

        # Calculate total revenue
        revenue_aggregate = Payment.objects.filter(
            status='paid'
        ).aggregate(total=Sum('amount'))
        total_revenue = revenue_aggregate['total'] or 0

        # Recent records
        recent_leads     = Lead.objects.order_by('-created_at')[:5]
        recent_customers = Customer.objects.order_by('-created_at')[:5]

        # Leads breakdown by status — for donut chart
        leads_new       = Lead.objects.filter(status='new').count()
        leads_contacted = Lead.objects.filter(status='contacted').count()
        leads_qualified = Lead.objects.filter(status='qualified').count()
        leads_proposal  = Lead.objects.filter(status='proposal').count()
        leads_won       = Lead.objects.filter(status='won').count()

        # Update context
        dashboard_context.update({
            'total_leads':         total_leads,
            'total_customers':     total_customers,
            'total_quotations':    total_quotations,
            'total_installations': total_installations,
            'pending_payments':    pending_payments,
            'total_revenue':       total_revenue,
            'recent_leads':        recent_leads,
            'recent_customers':    recent_customers,
            'leads_new':           leads_new,
            'leads_contacted':     leads_contacted,
            'leads_qualified':     leads_qualified,
            'leads_proposal':      leads_proposal,
            'leads_won':           leads_won,
        })

    except Exception as error:
        print(f"Dashboard error: {error}")

    # Task counts — separate try so dashboard never crashes
    try:
        from tasks.models import Task
        today_date   = timezone.now().date()
        task_today   = Task.objects.filter(
            due_date=today_date,
            status__in=['pending', 'in_progress']
        )
        task_overdue = Task.objects.filter(status='overdue')

        if not request.user.is_superuser:
            task_today   = task_today.filter(assigned_to=request.user)
            task_overdue = task_overdue.filter(assigned_to=request.user)

        dashboard_context.update({
            'task_today':   task_today.count(),
            'task_overdue': task_overdue.count(),
        })
    except Exception as error:
        print(f"Task counts error: {error}")

    return render(request, 'dashboard/dashboard.html', dashboard_context)


@login_required(login_url='/accounts/login/')
def dashboard_stats_api(request):
    """AJAX endpoint — returns live dashboard stat counts as JSON."""

    from leads.models import Lead
    from customers.models import Customer
    from quotations.models import Quotation
    from installations.models import Installation
    from payments.models import Payment

    # Task counts
    try:
        from tasks.models import Task
        today_date   = timezone.now().date()
        task_today   = Task.objects.filter(
            due_date=today_date,
            status__in=['pending', 'in_progress']
        )
        task_overdue = Task.objects.filter(status='overdue')

        if not request.user.is_superuser:
            task_today   = task_today.filter(assigned_to=request.user)
            task_overdue = task_overdue.filter(assigned_to=request.user)

        task_today_count   = task_today.count()
        task_overdue_count = task_overdue.count()
    except Exception:
        task_today_count   = 0
        task_overdue_count = 0

    try:
        revenue_aggregate = Payment.objects.filter(
            status='paid'
        ).aggregate(total=Sum('amount'))

        data = {
            'total_leads':         Lead.objects.count(),
            'total_customers':     Customer.objects.count(),
            'total_quotations':    Quotation.objects.count(),
            'total_installations': Installation.objects.count(),
            'pending_payments':    Payment.objects.filter(status='unpaid').count(),
            'total_revenue':       str(revenue_aggregate['total'] or 0),
            'leads_new':           Lead.objects.filter(status='new').count(),
            'leads_contacted':     Lead.objects.filter(status='contacted').count(),
            'leads_qualified':     Lead.objects.filter(status='qualified').count(),
            'leads_proposal':      Lead.objects.filter(status='proposal').count(),
            'leads_won':           Lead.objects.filter(status='won').count(),
            'task_today':          task_today_count,
            'task_overdue':        task_overdue_count,
        }
        return JsonResponse({'success': True, 'data': data})

    except Exception as error:
        print(f"Dashboard stats API error: {error}")
        return JsonResponse({'success': False, 'error': str(error)}, status=500)


@login_required(login_url='/accounts/login/')
def update_lead_status_api(request, pk):
    """AJAX endpoint — updates a lead's status inline from the leads table."""

    from leads.models import Lead

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    try:
        body       = json.loads(request.body)
        new_status = body.get('status')

        # Validate against allowed statuses
        allowed = ['new', 'contacted', 'qualified', 'proposal', 'won', 'lost']
        if new_status not in allowed:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)

        lead        = get_object_or_404(Lead, pk=pk)
        lead.status = new_status
        lead.save()

        return JsonResponse({
            'success':      True,
            'status':       lead.status,
            'status_label': lead.get_status_display(),
        })

    except Exception as error:
        print(f"Update lead status error: {error}")
        return JsonResponse({'success': False, 'error': str(error)}, status=500)