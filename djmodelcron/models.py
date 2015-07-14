# encoding:utf8
from dateutil.rrule import (DAILY, HOURLY, MINUTELY, MONTHLY, SECONDLY, WEEKLY,
                            YEARLY, rrule)
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

FREQUENCY = (("YEARLY", _("Yearly")),
             ("MONTHLY", _("Monthly")),
             ("WEEKLY", _("Weekly")),
             ("DAILY", _("Daily")),
             ("HOURLY", _("Hourly")),
             ("MINUTELY", _("Minutely")),
             ("SECONDLY", _("Secondly")))


class Repetition(TimeStampedModel):
    title = models.CharField(blank=True, null=True, max_length=125)
    rule = models.CharField(max_length=15, choices=FREQUENCY)
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)
    end = models.DateTimeField(null=True, blank=True)

    def __unicode__(self,):
        if self.title:
            return self.title
        return self.pk

    def rrule_frequency(self):
        compatibiliy_dict = {
            'DAILY': DAILY,
            'MONTHLY': MONTHLY,
            'WEEKLY': WEEKLY,
            'YEARLY': YEARLY,
            'HOURLY': HOURLY,
            'MINUTELY': MINUTELY,
            'SECONDLY': SECONDLY
        }
        return compatibiliy_dict[self.rule]

    def get_rule(self, start):
        return rrule(self.rrule_frequency(), start)

    def get_ocurrences(self, dstart, start, end):
        if self.end and start > self.end:
            return None

        if self.end and end > self.end:
            end = self.end

        rule = self.get_rule(dstart)

        print "* Get from {} to {}".format(start, end)
        ocurrences = rule.between(start, end, inc=True)
        if ocurrences:
            return map(lambda x: x.astimezone(timezone.get_current_timezone()), ocurrences)
        return []


class Cron(TimeStampedModel):
    title = models.CharField(max_length=125)
    start = models.DateTimeField()
    enabled = models.BooleanField(default=True)

    repetition = models.ForeignKey(Repetition, null=True, blank=True)

    # Generic relation
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self,):
        if self.title:
            return self.title
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
