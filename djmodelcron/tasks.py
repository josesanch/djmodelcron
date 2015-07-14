from django.utils import timezone

from celery.Celery import task

from .models import Cron


@task()
def run_task(content_type, pk):
    cron = Cron.objects.get(pk=pk)
    cron.content_object.run()


@task(name="cron")
def cron():
    now = timezone.now().replace(second=0, microsecond=0)
    crones = Cron.objects.filter(enabled=True)

    for cron in crones:
        ocurrences = cron.in_minutes(now)
        for ocurrence in ocurrences:
            run_task.apply_async([cron.pk], eta=ocurrence)
