from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lead, LEAD_STATUS_CHOICES, LEAD_SOURCE_CHOICES

LOGIN_URL = '/accounts/login/'


@login_required(login_url=LOGIN_URL)
def leads_list_view(request):
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search_query:
        leads_queryset = Lead.objects.filter(
            name__icontains=search_query
        ) | Lead.objects.filter(
            phone__icontains=search_query
        ) | Lead.objects.filter(
            email__icontains=search_query
        )
        leads_queryset = leads_queryset.order_by('-created_at')
    else:
        leads_queryset = Lead.objects.all().order_by('-created_at')

    if status_filter:
        leads_queryset = leads_queryset.filter(status=status_filter)

    context = {
        'leads_list':     leads_queryset,
        'search_query':   search_query,
        'status_filter':  status_filter,
        'total_count':    leads_queryset.count(),
        'status_choices': LEAD_STATUS_CHOICES,
        'page_title':     'Leads',
    }
    return render(request, 'leads/leads_list.html', context)


@login_required(login_url=LOGIN_URL)
def leads_detail_view(request, lead_id):
    lead_instance = get_object_or_404(Lead, pk=lead_id)
    context = {
        'lead_instance': lead_instance,
        'page_title':    f'Lead — {lead_instance.name}',
    }
    return render(request, 'leads/leads_detail.html', context)


@login_required(login_url=LOGIN_URL)
def leads_add_view(request):
    if request.method == 'POST':
        lead_name    = request.POST.get('name', '').strip()
        lead_phone   = request.POST.get('phone', '').strip()
        lead_email   = request.POST.get('email', '').strip()
        lead_address = request.POST.get('address', '').strip()
        lead_source  = request.POST.get('source', '')
        lead_status  = request.POST.get('status', 'new')
        lead_notes   = request.POST.get('notes', '').strip()

        if not lead_name or not lead_phone:
            messages.error(request, 'Name and Phone are required fields.')
            return render(request, 'leads/leads_add.html', {
                'status_choices': LEAD_STATUS_CHOICES,
                'source_choices': LEAD_SOURCE_CHOICES,
                'page_title':     'Add Lead',
            })

        new_lead = Lead.objects.create(
            name    = lead_name,
            phone   = lead_phone,
            email   = lead_email,
            address = lead_address,
            source  = lead_source,
            status  = lead_status,
            notes   = lead_notes,
        )
        messages.success(request, f'Lead "{new_lead.name}" added successfully!')
        return redirect('leads_list_view')

    context = {
        'status_choices': LEAD_STATUS_CHOICES,
        'source_choices': LEAD_SOURCE_CHOICES,
        'page_title':     'Add Lead',
    }
    return render(request, 'leads/leads_add.html', context)


@login_required(login_url=LOGIN_URL)
def leads_edit_view(request, lead_id):
    lead_instance = get_object_or_404(Lead, pk=lead_id)

    if request.method == 'POST':
        lead_instance.name    = request.POST.get('name', '').strip()
        lead_instance.phone   = request.POST.get('phone', '').strip()
        lead_instance.email   = request.POST.get('email', '').strip()
        lead_instance.address = request.POST.get('address', '').strip()
        lead_instance.source  = request.POST.get('source', '')
        lead_instance.status  = request.POST.get('status', 'new')
        lead_instance.notes   = request.POST.get('notes', '').strip()
        lead_instance.save()
        messages.success(request, f'Lead "{lead_instance.name}" updated successfully!')
        return redirect('leads_list_view')

    context = {
        'lead_instance':  lead_instance,
        'status_choices': LEAD_STATUS_CHOICES,
        'source_choices': LEAD_SOURCE_CHOICES,
        'page_title':     f'Edit — {lead_instance.name}',
    }
    return render(request, 'leads/leads_edit.html', context)


@login_required(login_url=LOGIN_URL)
def leads_delete_view(request, lead_id):
    lead_instance = get_object_or_404(Lead, pk=lead_id)
    if request.method == 'POST':
        lead_name = lead_instance.name
        lead_instance.delete()
        messages.success(request, f'Lead "{lead_name}" deleted successfully!')
        return redirect('leads_list_view')
    context = {
        'lead_instance': lead_instance,
        'page_title':    f'Delete — {lead_instance.name}',
    }
    return render(request, 'leads/leads_delete.html', context)


@login_required(login_url=LOGIN_URL)
def leads_convert_view(request, lead_id):
    """Convert a qualified lead to a customer."""
    lead_instance = get_object_or_404(Lead, pk=lead_id)

    if request.method == 'POST':
        from customers.models import Customer

        # Check if customer already exists
        existing = Customer.objects.filter(
            phone=lead_instance.phone
        ).first()

        if existing:
            messages.warning(
                request,
                f'A customer with phone {lead_instance.phone} already exists: {existing.name}'
            )
            return redirect('leads_detail_view', lead_id=lead_id)

        # Create customer from lead data
        system_size = request.POST.get('system_size', '0') or '0'
        city        = request.POST.get('city', '').strip()

        new_customer = Customer.objects.create(
            name        = lead_instance.name,
            phone       = lead_instance.phone,
            email       = lead_instance.email,
            address     = lead_instance.address,
            city        = city,
            system_size = system_size,
        )

        # Update lead status to qualified
        lead_instance.status = 'qualified'
        lead_instance.notes  = (
            lead_instance.notes +
            f'\n[Converted to Customer on {new_customer.created_at.strftime("%d %b %Y")}]'
        ).strip()
        lead_instance.save()

        messages.success(
            request,
            f'Lead "{lead_instance.name}" successfully converted to customer!'
        )
        return redirect('customers_list_view')

    context = {
        'lead_instance': lead_instance,
        'page_title':    f'Convert — {lead_instance.name}',
    }
    return render(request, 'leads/leads_convert.html', context)