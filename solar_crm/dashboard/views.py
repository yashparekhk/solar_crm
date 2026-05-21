"""
Dashboard views.
Naming Convention:
  - Function names: snake_case ending with '_view'
  - Variables: snake_case
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


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
    }

    # Import models safely
    try:
        from leads.models import Lead
        from customers.models import Customer
        from quotations.models import Quotation
        from installations.models import Installation
        from payments.models import Payment

        # Count stats — snake_case variable names
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
        # Log error silently — don't crash dashboard
        print(f"Dashboard error: {error}")

    return render(request, 'dashboard/dashboard.html', dashboard_context)