# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import logging
from celery.result import AsyncResult

from threedi_task.models import Task


logger = logging.getLogger(__name__)

SUCCESS_STATES = ['SUCCESS']
FAILURE_STATES = ['FAILURE']


def update_task_status(
        task_name=None, success_states=SUCCESS_STATES,
        failure_states=FAILURE_STATES, *args, **kwargs):
    """Check the state of the tasks and update it"""
    excluded_states = success_states + failure_states

    # First get all the outstanding tasks from the db
    tasks = Task.objects.filter(name=task_name) if task_name else \
        Task.objects.all()
    outstanding_tasks = tasks.exclude(state__in=excluded_states)

    task_ids = [t.uuid for t in outstanding_tasks]

    async_results = [AsyncResult(tid) for tid in task_ids]

    # Check if the outstanding tasks have succeeded
    succeeded = []
    for ar in async_results:
        state = ar.state
        ready = ar.ready()  # TODO: useful as extra check?

        if state in success_states:
            task_id = ar.id  # same as uuid
            t = Task.objects.get(uuid=task_id)
            t.state = str(ar.state)
            t.save()
            succeeded.append(task_id)

    return succeeded
