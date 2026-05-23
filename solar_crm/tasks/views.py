"""
Tasks / Follow-up Module views.
"""

from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib                 import messages
from django.http                    import JsonResponse
from django.utils                   import timezone
import json

from .models import Task
from django.contrib.auth import get_user_model
User = get_user_model()


def get_perms(user):
    is_admin    = user.is_superuser or getattr(user, 'role', '') == 'admin'
    is_employee = not is_admin
    return {
        'is_admin':            is_admin,
        'is_employee':         is_employee,
        'can_import':          is_admin,
        'can_manage_users':    is_admin,
        'can_create_lead':     True,
        'can_assign_lead':     is_admin,
        'can_delete_lead':     is_admin,
        'can_edit_payment':    is_admin,
        'can_delete_payment':  is_admin,
    }


# ── LIST ──────────────────────────────────────────────────────────────────────
@login_required(login_url='/accounts/login/')
def tasks_list_view(request):
    perms = get_perms(request.user)
    today = timezone.now().date()

    # Auto-mark overdue
    Task.objects.filter(
        due_date__lt=today,
        status__in=['pending', 'in_progress']
    ).update(status='overdue')

    if perms['is_admin']:
        all_tasks = Task.objects.select_related(
            'assigned_to', 'created_by', 'related_lead', 'related_customer'
        )
    else:
        all_tasks = Task.objects.filter(
            assigned_to=request.user
        ).select_related('assigned_to', 'created_by', 'related_lead', 'related_customer')

    # Filter tabs
    tab = request.GET.get('tab', 'all')
    if tab == 'today':
        tasks = all_tasks.filter(due_date=today)
    elif tab == 'overdue':
        tasks = all_tasks.filter(status='overdue')
    elif tab == 'completed':
        tasks = all_tasks.filter(status='completed')
    elif tab == 'pending':
        tasks = all_tasks.filter(status__in=['pending', 'in_progress'])
    else:
        tasks = all_tasks

    # Counts for tab badges
    counts = {
        'all':       all_tasks.count(),
        'today':     all_tasks.filter(due_date=today).count(),
        'overdue':   all_tasks.filter(status='overdue').count(),
        'pending':   all_tasks.filter(status__in=['pending', 'in_progress']).count(),
        'completed': all_tasks.filter(status='completed').count(),
    }

    context = {
        'tasks':     tasks,
        'tab':       tab,
        'counts':    counts,
        'today':     today,
        'perms_map': perms,
    }
    return render(request, 'tasks/tasks_list.html', context)


# ── ADD ───────────────────────────────────────────────────────────────────────
@login_required(login_url='/accounts/login/')
def tasks_add_view(request):
    perms = get_perms(request.user)

    try:
        from leads.models import Lead
        leads = Lead.objects.all()
    except Exception:
        leads = []

    try:
        from customers.models import Customer
        customers = Customer.objects.all()
    except Exception:
        customers = []

    users = User.objects.filter(is_active=True)

    if request.method == 'POST':
        title          = request.POST.get('title', '').strip()
        description    = request.POST.get('description', '').strip()
        task_type      = request.POST.get('task_type', 'task')
        priority       = request.POST.get('priority', 'medium')
        due_date       = request.POST.get('due_date')
        due_time       = request.POST.get('due_time') or None
        assigned_to_id = request.POST.get('assigned_to')
        related_lead_id  = request.POST.get('related_lead') or None
        related_cust_id  = request.POST.get('related_customer') or None

        if not title or not due_date or not assigned_to_id:
            messages.error(request, 'Title, due date and assigned user are required.')
        else:
            assigned_user = get_object_or_404(User, pk=assigned_to_id)
            Task.objects.create(
                title               = title,
                description         = description,
                task_type           = task_type,
                priority            = priority,
                due_date            = due_date,
                due_time            = due_time,
                assigned_to         = assigned_user,
                created_by          = request.user,
                related_lead_id     = related_lead_id,
                related_customer_id = related_cust_id,
            )
            messages.success(request, f'Task "{title}" created successfully.')
            return redirect('tasks_list_view')

    context = {
        'leads':     leads,
        'customers': customers,
        'users':     users,
        'perms_map': perms,
        'today':     timezone.now().date().isoformat(),
    }
    return render(request, 'tasks/tasks_add.html', context)


# ── EDIT ──────────────────────────────────────────────────────────────────────
@login_required(login_url='/accounts/login/')
def tasks_edit_view(request, pk):
    perms = get_perms(request.user)
    task  = get_object_or_404(Task, pk=pk)

    if not perms['is_admin'] and task.assigned_to != request.user:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('tasks_list_view')

    try:
        from leads.models import Lead
        leads = Lead.objects.all()
    except Exception:
        leads = []

    try:
        from customers.models import Customer
        customers = Customer.objects.all()
    except Exception:
        customers = []

    users = User.objects.filter(is_active=True)

    if request.method == 'POST':
        task.title       = request.POST.get('title', '').strip()
        task.description = request.POST.get('description', '').strip()
        task.task_type   = request.POST.get('task_type', 'task')
        task.priority    = request.POST.get('priority', 'medium')
        task.status      = request.POST.get('status', 'pending')
        task.due_date    = request.POST.get('due_date')
        task.due_time    = request.POST.get('due_time') or None
        assigned_to_id   = request.POST.get('assigned_to')
        task.related_lead_id     = request.POST.get('related_lead') or None
        task.related_customer_id = request.POST.get('related_customer') or None

        if assigned_to_id:
            task.assigned_to = get_object_or_404(User, pk=assigned_to_id)

        if task.status == 'completed' and not task.completed_at:
            task.completed_at = timezone.now()

        task.save()
        messages.success(request, f'Task "{task.title}" updated.')
        return redirect('tasks_list_view')

    context = {
        'task':      task,
        'leads':     leads,
        'customers': customers,
        'users':     users,
        'perms_map': perms,
    }
    return render(request, 'tasks/tasks_edit.html', context)


# ── DELETE ────────────────────────────────────────────────────────────────────
@login_required(login_url='/accounts/login/')
def tasks_delete_view(request, pk):
    perms = get_perms(request.user)
    task  = get_object_or_404(Task, pk=pk)

    if not perms['is_admin']:
        messages.error(request, 'Only admins can delete tasks.')
        return redirect('tasks_list_view')

    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted.')
        return redirect('tasks_list_view')

    context = {
        'task':      task,
        'perms_map': perms,
    }
    return render(request, 'tasks/tasks_delete.html', context)


# ── AJAX: Mark complete ───────────────────────────────────────────────────────
@login_required(login_url='/accounts/login/')
def tasks_complete_api(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)

    task  = get_object_or_404(Task, pk=pk)
    perms = get_perms(request.user)

    if not perms['is_admin'] and task.assigned_to != request.user:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

    task.status       = 'completed'
    task.completed_at = timezone.now()
    task.save()
    return JsonResponse({'success': True})


# ── AJAX: Update task status ──────────────────────────────────────────────────
@login_required(login_url='/accounts/login/')
def tasks_status_api(request, pk):
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)

    task  = get_object_or_404(Task, pk=pk)
    perms = get_perms(request.user)

    if not perms['is_admin'] and task.assigned_to != request.user:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

    try:
        body       = json.loads(request.body)
        new_status = body.get('status')

        allowed = ['pending', 'in_progress', 'completed', 'overdue']
        if new_status not in allowed:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)

        task.status = new_status
        if new_status == 'completed' and not task.completed_at:
            task.completed_at = timezone.now()
        task.save()

        return JsonResponse({
            'success':      True,
            'status':       task.status,
            'status_label': task.get_status_display(),
        })

    except Exception as error:
        return JsonResponse({'success': False, 'error': str(error)}, status=500)


# ── AJAX: Dashboard widget ────────────────────────────────────────────────────
@login_required(login_url='/accounts/login/')
def tasks_widget_api(request):
    today = timezone.now().date()
    perms = get_perms(request.user)

    qs = Task.objects.all() if perms['is_admin'] else Task.objects.filter(
        assigned_to=request.user
    )

    data = {
        'today':     qs.filter(due_date=today, status__in=['pending', 'in_progress']).count(),
        'overdue':   qs.filter(status='overdue').count(),
        'pending':   qs.filter(status__in=['pending', 'in_progress']).count(),
        'completed': qs.filter(status='completed').count(),
    }
    return JsonResponse({'success': True, 'data': data})