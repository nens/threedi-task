# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin

from threedi_task import models


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('start_time',)  # or else it doesn't appear in admin

admin.site.register(models.Task, TaskAdmin)
