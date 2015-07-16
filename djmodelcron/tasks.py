from django.utils import timezone

import celery
from celery.schedules import crontab

from .models import Cron


@celery.task(name='run_task')
def run_task(pk):
    cron = Cron.objects.get(pk=pk)
    cron.content_object.run()


@celery.decorators.periodic_task(name="cron", run_every=crontab())
def cron():
    now = timezone.now().replace(second=0, microsecond=0)
    crones = Cron.objects.filter(enabled=True)
    for cron in crones:
        ocurrences = cron.in_minutes(now)
        for ocurrence in ocurrences:
            run_task.apply_async([cron.pk])
