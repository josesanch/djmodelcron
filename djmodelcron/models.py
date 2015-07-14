# encoding:utf8
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from recurrence.fields import RecurrenceField


class Cron(models.Model):
    enabled = models.BooleanField(default=True)
    start = models.DateTimeField()
    recurrences = RecurrenceField()

    # Generic relation
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self,):

        return self.pk

    def get_ocurrences(self, start, end=None):
        if not self.repetition and self.start > start:
            return []

        return self.repetition.get_ocurrences(self.start, start, end)

    def in_minutes(self, start=None, minutes=1):
        if not start:
            start = timezone.now()

        end = start + timezone.timedelta(minutes=minutes)
        return self.get_ocurrences(start, end)
