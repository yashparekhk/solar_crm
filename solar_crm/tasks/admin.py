from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ['title', 'task_type', 'priority', 'status', 'assigned_to', 'due_date']
    list_filter   = ['status', 'priority', 'task_type']
    search_fields = ['title', 'description']