from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

class Command(BaseCommand):
    help = 'Создаёт еженедельную задачу рассылки новостей'

    def handle(self, *args, **kwargs):
        schedule, _ = CrontabSchedule.objects.get_or_create(minute='0', hour='8', day_of_week='1')
        task, created = PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='Weekly news digest',
            task='news.tasks.send_weekly_digest',
            defaults={'kwargs': json.dumps({})}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Периодическая задача создана!'))
        else:
            self.stdout.write(self.style.WARNING('Задача уже существует.'))
