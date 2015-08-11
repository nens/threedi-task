# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import datetime
from collections import namedtuple

from django.db import models
from django.contrib.auth.models import User
from celery.result import AsyncResult
# from django.utils.translation import ugettext_lazy as _

import requests

# see Celery source
SUCCESS_STATES = ['SUCCESS']
FAILURE_STATES = ['FAILURE', 'REVOKED']
READY_STATES = SUCCESS_STATES + FAILURE_STATES


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

    def update_state_async_result(self):
        """Update state and end_time if ready via Celery AsyncResult."""
        previous_state = self.state

        async_result = AsyncResult(self.uuid)
        assert async_result.id == self.uuid
        new_state = async_result.state

        # ready means SUCCESS, FAILURE or REVOKED (see Celery source code)
        ready = async_result.ready()
        if ready:
            self.end_time = datetime.datetime.now()
            self.result = async_result.result

        self.state = str(new_state)
        self.save()

        State = namedtuple('State', ['previous_state', 'new_state', 'ready'])
        return State(previous_state, new_state, ready)

    def update_state_djcelery_api(self, base_url):
        """
        Update state using a call to the status URL implemented via the
        djcelery views
        """
        previous_state = self.state
        url = "{base_url}/{task_id}/status".format(base_url=base_url,
                                                   task_id=self.uuid)
        r = requests.get(url)
        resp = r.json()
        new_state = resp['task']['status']

        ready = new_state in READY_STATES
        if ready:
            self.end_time = datetime.datetime.now()
            self.result = resp['task']['result']

        self.state = str(new_state)
        self.save()

        State = namedtuple('State', ['previous_state', 'new_state', 'ready'])
        return State(previous_state, new_state, ready)
