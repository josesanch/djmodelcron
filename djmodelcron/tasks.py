from django.utils import timezone

from celery_app import app
from erpnotify.models import Tarea

from .models import Cron


@app.task()
def run_tarea(tarea_id):
    tarea = Tarea.objects.get(pk=tarea_id)
    tarea.run()


@app.task(name="cron")
def cron():
    now = timezone.now().replace(second=0, microsecond=0)
    print "* CRON {}".format(now)
    crones = Cron.objects.filter(enabled=True)
    print crones
    for cron in crones:
        ocurrences = cron.in_minutes(now)
        for ocurrence in ocurrences:
            print cron.content_object
            run_tarea.apply_async([cron.content_object.pk], eta=ocurrence)
