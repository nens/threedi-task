# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models
from django.contrib.auth.models import User
from celery.result import AsyncResult
# from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    """A representation of a Celery task"""
    uuid = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    state = models.CharField(max_length=20)
    args = models.TextField(blank=True)
    kwargs = models.TextField(blank=True)
    result = models.TextField(blank=True)

    # the time the task was called or requested, which is a local time; this
    # differs from the 'received' and 'started' time in Celery flower which
    # refers to the the time in which Celery picks up or executes the task
    start_time = models.DateTimeField(auto_now_add=True)

    end_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        get_latest_by = "start_time"
        ordering = ("-start_time",)

    def __unicode__(self):
        return "{} ({})".format(self.name, self.uuid)

    def update_state(self):
        async_result = AsyncResult(self.uuid)

        assert async_result.id == self.uuid

        old_state = self.state
        new_state = async_result.state
        ready = async_result.ready()  # TODO: useful as extra check?
        self.state = str(new_state)
        self.save()

        return old_state, new_state, ready
