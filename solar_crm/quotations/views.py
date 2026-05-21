from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Quotation, QUOTATION_STATUS_CHOICES
from customers.models import Customer

LOGIN_URL = '/accounts/login/'


@login_required(login_url=LOGIN_URL)
def quotations_list_view(request):
    quotations_queryset = Quotation.objects.all().order_by('-created_at')
    context = {
        'quotations_list': quotations_queryset,
        'total_count':     quotations_queryset.count(),
        'page_title':      'Quotations',
    }
    return render(request, 'quotations/quotations_list.html', context)


@login_required(login_url=LOGIN_URL)
def quotations_detail_view(request, quotation_id):
    quotation_instance = get_object_or_404(Quotation, pk=quotation_id)
    context = {
        'quotation_instance': quotation_instance,
        'page_title':         f'Quotation — {quotation_instance.quotation_no}',
    }
    return render(request, 'quotations/quotations_detail.html', context)


@login_required(login_url=LOGIN_URL)
def quotations_add_view(request):
    customers_queryset = Customer.objects.all()
    if request.method == 'POST':
        Quotation.objects.create(
            customer_id  = request.POST.get('customer'),
            quotation_no = request.POST.get('quotation_no', '').strip(),
            system_size  = request.POST.get('system_size', '0'),
            total_amount = request.POST.get('total_amount', '0'),
            status       = request.POST.get('status', 'draft'),
            notes        = request.POST.get('notes', '').strip(),
        )
        messages.success(request, 'Quotation added successfully!')
        return redirect('quotations_list_view')
    context = {
        'customers_list': customers_queryset,
        'status_choices': QUOTATION_STATUS_CHOICES,
        'page_title':     'Add Quotation',
    }
    return render(request, 'quotations/quotations_add.html', context)


@login_required(login_url=LOGIN_URL)
def quotations_edit_view(request, quotation_id):
    quotation_instance = get_object_or_404(Quotation, pk=quotation_id)
    customers_queryset = Customer.objects.all()
    if request.method == 'POST':
        quotation_instance.customer_id  = request.POST.get('customer')
        quotation_instance.system_size  = request.POST.get('system_size', '0')
        quotation_instance.total_amount = request.POST.get('total_amount', '0')
        quotation_instance.status       = request.POST.get('status', 'draft')
        quotation_instance.notes        = request.POST.get('notes', '').strip()
        quotation_instance.save()
        messages.success(request, 'Quotation updated successfully!')
        return redirect('quotations_list_view')
    context = {
        'quotation_instance': quotation_instance,
        'customers_list':     customers_queryset,
        'status_choices':     QUOTATION_STATUS_CHOICES,
        'page_title':         f'Edit — {quotation_instance.quotation_no}',
    }
    return render(request, 'quotations/quotations_edit.html', context)


@login_required(login_url=LOGIN_URL)
def quotations_delete_view(request, quotation_id):
    quotation_instance = get_object_or_404(Quotation, pk=quotation_id)
    if request.method == 'POST':
        quotation_instance.delete()
        messages.success(request, 'Quotation deleted!')
        return redirect('quotations_list_view')
    context = {
        'quotation_instance': quotation_instance,
        'page_title':         'Delete Quotation',
    }
    return render(request, 'quotations/quotations_delete.html', context)