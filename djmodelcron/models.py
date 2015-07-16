# encoding:utf8
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from recurrence.fields import RecurrenceField


class Cron(models.Model):
    enabled = models.BooleanField(default=True)
    start = models.DateTimeField()
    recurrence = RecurrenceField()

    # Generic relation
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def get_ocurrences(self, start, end=None):
        return self.recurrence.between(start,
                                       end,
                                       dtstart=self.start,
                                       inc=True)

    def in_minutes(self, start=None, minutes=1):
        if not start:
            start = timezone.now()

        end = start + timezone.timedelta(minutes=minutes)
        return self.get_ocurrences(start, end)
