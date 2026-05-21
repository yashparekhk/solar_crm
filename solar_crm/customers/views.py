from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer

LOGIN_URL = '/accounts/login/'


@login_required(login_url=LOGIN_URL)
def customers_list_view(request):
    search_query = request.GET.get('q', '').strip()
    if search_query:
        customers_queryset = Customer.objects.filter(
            name__icontains=search_query
        ) | Customer.objects.filter(
            phone__icontains=search_query
        ) | Customer.objects.filter(
            city__icontains=search_query
        )
        customers_queryset = customers_queryset.order_by('-created_at')
    else:
        customers_queryset = Customer.objects.all().order_by('-created_at')

    context = {
        'customers_list': customers_queryset,
        'search_query':   search_query,
        'total_count':    customers_queryset.count(),
        'page_title':     'Customers',
    }
    return render(request, 'customers/customers_list.html', context)


@login_required(login_url=LOGIN_URL)
def customers_detail_view(request, customer_id):
    customer_instance = get_object_or_404(Customer, pk=customer_id)
    from quotations.models import Quotation
    from installations.models import Installation
    from payments.models import Payment
    customer_quotations    = Quotation.objects.filter(customer=customer_instance).order_by('-created_at')
    customer_installations = Installation.objects.filter(customer=customer_instance).order_by('-created_at')
    customer_payments      = Payment.objects.filter(customer=customer_instance).order_by('-created_at')
    context = {
        'customer_instance':     customer_instance,
        'customer_quotations':   customer_quotations,
        'customer_installations':customer_installations,
        'customer_payments':     customer_payments,
        'page_title':            f'Customer — {customer_instance.name}',
    }
    return render(request, 'customers/customers_detail.html', context)


@login_required(login_url=LOGIN_URL)
def customers_add_view(request):
    if request.method == 'POST':
        customer_name        = request.POST.get('name', '').strip()
        customer_phone       = request.POST.get('phone', '').strip()
        customer_email       = request.POST.get('email', '').strip()
        customer_address     = request.POST.get('address', '').strip()
        customer_city        = request.POST.get('city', '').strip()
        customer_system_size = request.POST.get('system_size', '0')
        if not customer_name or not customer_phone:
            messages.error(request, 'Name and Phone are required.')
            return render(request, 'customers/customers_add.html', {'page_title': 'Add Customer'})
        new_customer = Customer.objects.create(
            name=customer_name, phone=customer_phone, email=customer_email,
            address=customer_address, city=customer_city, system_size=customer_system_size,
        )
        messages.success(request, f'Customer "{new_customer.name}" added successfully!')
        return redirect('customers_list_view')
    return render(request, 'customers/customers_add.html', {'page_title': 'Add Customer'})


@login_required(login_url=LOGIN_URL)
def customers_edit_view(request, customer_id):
    customer_instance = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer_instance.name        = request.POST.get('name', '').strip()
        customer_instance.phone       = request.POST.get('phone', '').strip()
        customer_instance.email       = request.POST.get('email', '').strip()
        customer_instance.address     = request.POST.get('address', '').strip()
        customer_instance.city        = request.POST.get('city', '').strip()
        customer_instance.system_size = request.POST.get('system_size', '0')
        customer_instance.save()
        messages.success(request, f'Customer "{customer_instance.name}" updated!')
        return redirect('customers_list_view')
    context = {
        'customer_instance': customer_instance,
        'page_title':        f'Edit — {customer_instance.name}',
    }
    return render(request, 'customers/customers_edit.html', context)


@login_required(login_url=LOGIN_URL)
def customers_delete_view(request, customer_id):
    customer_instance = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer_name = customer_instance.name
        customer_instance.delete()
        messages.success(request, f'Customer "{customer_name}" deleted!')
        return redirect('customers_list_view')
    context = {
        'customer_instance': customer_instance,
        'page_title':        f'Delete — {customer_instance.name}',
    }
    return render(request, 'customers/customers_delete.html', context)