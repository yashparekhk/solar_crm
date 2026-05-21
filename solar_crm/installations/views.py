from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Installation, INSTALLATION_STATUS_CHOICES
from customers.models import Customer

LOGIN_URL = '/accounts/login/'


@login_required(login_url=LOGIN_URL)
def installations_list_view(request):
    installations_queryset = Installation.objects.all().order_by('-created_at')
    context = {
        'installations_list': installations_queryset,
        'total_count':        installations_queryset.count(),
        'page_title':         'Installations',
    }
    return render(request, 'installations/installations_list.html', context)


@login_required(login_url=LOGIN_URL)
def installations_detail_view(request, installation_id):
    installation_instance = get_object_or_404(Installation, pk=installation_id)
    context = {
        'installation_instance': installation_instance,
        'page_title':            f'Installation — {installation_instance.customer.name}',
    }
    return render(request, 'installations/installations_detail.html', context)


@login_required(login_url=LOGIN_URL)
def installations_add_view(request):
    customers_queryset = Customer.objects.all()
    if request.method == 'POST':
        Installation.objects.create(
            customer_id = request.POST.get('customer'),
            system_size = request.POST.get('system_size', '0'),
            start_date  = request.POST.get('start_date'),
            end_date    = request.POST.get('end_date') or None,
            status      = request.POST.get('status', 'scheduled'),
            technician  = request.POST.get('technician', '').strip(),
            notes       = request.POST.get('notes', '').strip(),
        )
        messages.success(request, 'Installation added successfully!')
        return redirect('installations_list_view')
    context = {
        'customers_list': customers_queryset,
        'status_choices': INSTALLATION_STATUS_CHOICES,
        'page_title':     'Add Installation',
    }
    return render(request, 'installations/installations_add.html', context)


@login_required(login_url=LOGIN_URL)
def installations_edit_view(request, installation_id):
    installation_instance = get_object_or_404(Installation, pk=installation_id)
    customers_queryset    = Customer.objects.all()
    if request.method == 'POST':
        installation_instance.customer_id = request.POST.get('customer')
        installation_instance.system_size = request.POST.get('system_size', '0')
        installation_instance.start_date  = request.POST.get('start_date')
        installation_instance.end_date    = request.POST.get('end_date') or None
        installation_instance.status      = request.POST.get('status', 'scheduled')
        installation_instance.technician  = request.POST.get('technician', '').strip()
        installation_instance.notes       = request.POST.get('notes', '').strip()
        installation_instance.save()
        messages.success(request, 'Installation updated!')
        return redirect('installations_list_view')
    context = {
        'installation_instance': installation_instance,
        'customers_list':        customers_queryset,
        'status_choices':        INSTALLATION_STATUS_CHOICES,
        'page_title':            'Edit Installation',
    }
    return render(request, 'installations/installations_edit.html', context)


@login_required(login_url=LOGIN_URL)
def installations_delete_view(request, installation_id):
    installation_instance = get_object_or_404(Installation, pk=installation_id)
    if request.method == 'POST':
        installation_instance.delete()
        messages.success(request, 'Installation deleted!')
        return redirect('installations_list_view')
    context = {
        'installation_instance': installation_instance,
        'page_title':            'Delete Installation',
    }
    return render(request, 'installations/installations_delete.html', context)