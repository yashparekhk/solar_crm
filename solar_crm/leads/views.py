from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lead, LEAD_STATUS_CHOICES, LEAD_SOURCE_CHOICES
from accounts.permissions import admin_required, employee_or_admin_required

LOGIN_URL = '/accounts/login/'


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def leads_list_view(request):
    """
    Admin sees all leads.
    Employee sees only assigned leads.
    """
    user = request.user

    if user.role == 'admin':
        leads_queryset = Lead.objects.all().order_by('-created_at')
    else:
        # Employee sees only their assigned leads
        leads_queryset = Lead.objects.filter(
            assigned_to=user
        ).order_by('-created_at')

    from accounts.models import CustomUser
    employees_list = CustomUser.objects.filter(
        role__in=['admin', 'employee']
    )

    context = {
        'leads_list':     leads_queryset,
        'total_count':    leads_queryset.count(),
        'status_choices': LEAD_STATUS_CHOICES,
        'employees_list': employees_list,
        'page_title':     'Leads',
    }
    return render(request, 'leads/leads_list.html', context)


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def leads_detail_view(request, lead_id):
    """Anyone can view lead if admin or assigned employee."""
    user          = request.user
    lead_instance = get_object_or_404(Lead, pk=lead_id)

    # Employee can only view assigned leads
    if user.role == 'employee' and lead_instance.assigned_to != user:
        messages.error(request, 'You do not have access to this lead.')
        return redirect('leads_list_view')

    context = {
        'lead_instance': lead_instance,
        'page_title':    f'Lead — {lead_instance.name}',
    }
    return render(request, 'leads/leads_detail.html', context)


@login_required(login_url=LOGIN_URL)
@admin_required
def leads_add_view(request):
    """Only admin can create leads."""
    from accounts.models import CustomUser
    employees_list = CustomUser.objects.filter(role__in=['admin', 'employee'])

    if request.method == 'POST':
        lead_name      = request.POST.get('name', '').strip()
        lead_phone     = request.POST.get('phone', '').strip()
        lead_email     = request.POST.get('email', '').strip()
        lead_address   = request.POST.get('address', '').strip()
        lead_source    = request.POST.get('source', '')
        lead_status    = request.POST.get('status', 'new')
        lead_notes     = request.POST.get('notes', '').strip()
        assigned_to_id = request.POST.get('assigned_to') or None

        if not lead_name or not lead_phone:
            messages.error(request, 'Name and Phone are required.')
            return render(request, 'leads/leads_add.html', {
                'status_choices': LEAD_STATUS_CHOICES,
                'source_choices': LEAD_SOURCE_CHOICES,
                'employees_list': employees_list,
                'page_title':     'Add Lead',
            })

        new_lead = Lead.objects.create(
            name           = lead_name,
            phone          = lead_phone,
            email          = lead_email,
            address        = lead_address,
            source         = lead_source,
            status         = lead_status,
            notes          = lead_notes,
            assigned_to_id = assigned_to_id,
        )
        messages.success(request, f'Lead "{new_lead.name}" created and assigned successfully!')
        return redirect('leads_list_view')

    context = {
        'status_choices': LEAD_STATUS_CHOICES,
        'source_choices': LEAD_SOURCE_CHOICES,
        'employees_list': employees_list,
        'page_title':     'Add Lead',
    }
    return render(request, 'leads/leads_add.html', context)


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def leads_edit_view(request, lead_id):
    """
    Admin can edit any lead.
    Employee can edit only assigned leads.
    """
    user          = request.user
    lead_instance = get_object_or_404(Lead, pk=lead_id)

    # Check permission
    if not lead_instance.can_edit(user):
        messages.error(request, 'You can only edit leads assigned to you.')
        return redirect('leads_list_view')

    from accounts.models import CustomUser
    employees_list = CustomUser.objects.filter(role__in=['admin', 'employee'])

    if request.method == 'POST':
        lead_instance.name   = request.POST.get('name', '').strip()
        lead_instance.phone  = request.POST.get('phone', '').strip()
        lead_instance.email  = request.POST.get('email', '').strip()
        lead_instance.address = request.POST.get('address', '').strip()
        lead_instance.source = request.POST.get('source', '')
        lead_instance.status = request.POST.get('status', 'new')
        lead_instance.notes  = request.POST.get('notes', '').strip()

        # Only admin can reassign
        if user.role == 'admin':
            lead_instance.assigned_to_id = request.POST.get('assigned_to') or None

        lead_instance.save()
        messages.success(request, f'Lead "{lead_instance.name}" updated!')
        return redirect('leads_list_view')

    context = {
        'lead_instance':  lead_instance,
        'status_choices': LEAD_STATUS_CHOICES,
        'source_choices': LEAD_SOURCE_CHOICES,
        'employees_list': employees_list,
        'page_title':     f'Edit — {lead_instance.name}',
    }
    return render(request, 'leads/leads_edit.html', context)


@login_required(login_url=LOGIN_URL)
@admin_required
def leads_delete_view(request, lead_id):
    """Only admin can delete leads."""
    lead_instance = get_object_or_404(Lead, pk=lead_id)
    if request.method == 'POST':
        lead_name = lead_instance.name
        lead_instance.delete()
        messages.success(request, f'Lead "{lead_name}" deleted!')
        return redirect('leads_list_view')
    context = {
        'lead_instance': lead_instance,
        'page_title':    f'Delete — {lead_instance.name}',
    }
    return render(request, 'leads/leads_delete.html', context)


@login_required(login_url=LOGIN_URL)
@employee_or_admin_required
def leads_convert_view(request, lead_id):
    """Admin and assigned employee can convert lead."""
    user          = request.user
    lead_instance = get_object_or_404(Lead, pk=lead_id)

    if not lead_instance.can_edit(user):
        messages.error(request, 'You can only convert leads assigned to you.')
        return redirect('leads_list_view')

    if request.method == 'POST':
        from customers.models import Customer
        existing = Customer.objects.filter(phone=lead_instance.phone).first()
        if existing:
            messages.warning(request, f'Customer with phone {lead_instance.phone} already exists.')
            return redirect('leads_detail_view', lead_id=lead_id)

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
        lead_instance.status = 'qualified'
        lead_instance.notes  = (
            lead_instance.notes +
            f'\n[Converted to Customer on {new_customer.created_at.strftime("%d %b %Y")}]'
        ).strip()
        lead_instance.save()
        messages.success(request, f'Lead converted to customer successfully!')
        return redirect('customers_list_view')

    context = {
        'lead_instance': lead_instance,
        'page_title':    f'Convert — {lead_instance.name}',
    }
    return render(request, 'leads/leads_convert.html', context)


@login_required(login_url=LOGIN_URL)
@admin_required
def leads_assign_view(request, lead_id):
    """Admin can assign/reassign a lead to an employee."""
    lead_instance  = get_object_or_404(Lead, pk=lead_id)
    from accounts.models import CustomUser
    employees_list = CustomUser.objects.filter(role__in=['admin', 'employee'])

    if request.method == 'POST':
        assigned_to_id = request.POST.get('assigned_to') or None
        lead_instance.assigned_to_id = assigned_to_id
        lead_instance.save()

        if assigned_to_id:
            assigned_user = CustomUser.objects.get(pk=assigned_to_id)
            messages.success(
                request,
                f'Lead "{lead_instance.name}" assigned to {assigned_user.get_full_name()}!'
            )
        else:
            messages.success(request, f'Lead "{lead_instance.name}" unassigned.')
        return redirect('leads_detail_view', lead_id=lead_id)

    context = {
        'lead_instance':  lead_instance,
        'employees_list': employees_list,
        'page_title':     f'Assign Lead — {lead_instance.name}',
    }
    return render(request, 'leads/leads_assign.html', context)