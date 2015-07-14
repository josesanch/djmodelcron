from django.contrib import admin

from .models import Cron, Repetition

admin.site.register(Cron)
admin.site.register(Repetition)
