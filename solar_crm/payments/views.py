from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment, PAYMENT_STATUS_CHOICES, PAYMENT_METHOD_CHOICES
from customers.models import Customer

LOGIN_URL = '/accounts/login/'


@login_required(login_url=LOGIN_URL)
def payments_list_view(request):
    payments_queryset = Payment.objects.all().order_by('-created_at')
    context = {
        'payments_list': payments_queryset,
        'total_count':   payments_queryset.count(),
        'page_title':    'Payments',
    }
    return render(request, 'payments/payments_list.html', context)


@login_required(login_url=LOGIN_URL)
def payments_detail_view(request, payment_id):
    payment_instance = get_object_or_404(Payment, pk=payment_id)
    context = {
        'payment_instance': payment_instance,
        'page_title':       f'Payment — {payment_instance.customer.name}',
    }
    return render(request, 'payments/payments_detail.html', context)


@login_required(login_url=LOGIN_URL)
def payments_add_view(request):
    customers_queryset = Customer.objects.all()
    if request.method == 'POST':
        Payment.objects.create(
            customer_id  = request.POST.get('customer'),
            amount       = request.POST.get('amount', '0'),
            status       = request.POST.get('status', 'unpaid'),
            payment_date = request.POST.get('payment_date') or None,
            method       = request.POST.get('method', ''),
            notes        = request.POST.get('notes', '').strip(),
            created_by   = request.user,
        )
        messages.success(request, 'Payment added successfully!')
        return redirect('payments_list_view')
    context = {
        'customers_list': customers_queryset,
        'status_choices': PAYMENT_STATUS_CHOICES,
        'method_choices': PAYMENT_METHOD_CHOICES,
        'page_title':     'Add Payment',
    }
    return render(request, 'payments/payments_add.html', context)


@login_required(login_url=LOGIN_URL)
def payments_edit_view(request, payment_id):
    payment_instance   = get_object_or_404(Payment, pk=payment_id)
    customers_queryset = Customer.objects.all()
    if request.method == 'POST':
        payment_instance.customer_id  = request.POST.get('customer')
        payment_instance.amount       = request.POST.get('amount', '0')
        payment_instance.status       = request.POST.get('status', 'unpaid')
        payment_instance.payment_date = request.POST.get('payment_date') or None
        payment_instance.method       = request.POST.get('method', '')
        payment_instance.notes        = request.POST.get('notes', '').strip()
        payment_instance.save()
        messages.success(request, 'Payment updated!')
        return redirect('payments_list_view')
    context = {
        'payment_instance': payment_instance,
        'customers_list':   customers_queryset,
        'status_choices':   PAYMENT_STATUS_CHOICES,
        'method_choices':   PAYMENT_METHOD_CHOICES,
        'page_title':       'Edit Payment',
    }
    return render(request, 'payments/payments_edit.html', context)


@login_required(login_url=LOGIN_URL)
def payments_delete_view(request, payment_id):
    payment_instance = get_object_or_404(Payment, pk=payment_id)
    if request.method == 'POST':
        payment_instance.delete()
        messages.success(request, 'Payment deleted!')
        return redirect('payments_list_view')
    context = {
        'payment_instance': payment_instance,
        'page_title':       'Delete Payment',
    }
    return render(request, 'payments/payments_delete.html', context)