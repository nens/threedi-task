# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.contrib import admin

from threedi_task import models


#class TaskManager(admin.ModelAdmin):
#    pass

admin.site.register(models.Task)
