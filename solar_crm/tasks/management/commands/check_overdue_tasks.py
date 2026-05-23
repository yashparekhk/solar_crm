from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task


class Command(BaseCommand):
    help = 'Marks overdue tasks and prints alerts'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        # Mark overdue
        overdue_updated = Task.objects.filter(
            due_date__lt=today,
            status__in=['pending', 'in_progress']
        ).update(status='overdue')

        self.stdout.write(
            self.style.WARNING(f'{overdue_updated} tasks marked as overdue.')
        )

        # Print today's pending tasks as reminders
        today_tasks = Task.objects.filter(
            due_date=today,
            status__in=['pending', 'in_progress']
        ).select_related('assigned_to')

        self.stdout.write(self.style.SUCCESS(f'\nToday\'s tasks ({today_tasks.count()}):'))
        for task in today_tasks:
            self.stdout.write(
                f'  [{task.priority.upper()}] {task.title} → {task.assigned_to.get_full_name()}'
            )