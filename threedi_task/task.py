# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import logging

from django.conf import settings

from threedi_task.models import Task


logger = logging.getLogger(__name__)


def update_task_states(
        task_name=None, success_states=settings.SUCCESS_STATES,
        failure_states=settings.FAILURE_STATES, *args, **kwargs):
    """Check the state of the tasks and update it

    Params:
        task_name: a specific task name to update, if None: update all tasks
        success_states: states which count as success
        failure_states: states which count as failed (will be excluded)
    Returns:
        a list of succeeded tasks
    """
    excluded_states = success_states + failure_states

    # First get all the outstanding tasks from the db
    tasks = Task.objects.filter(name=task_name) if task_name else \
        Task.objects.all()
    outstanding_tasks = tasks.exclude(state__in=excluded_states)

    # Check if the outstanding tasks have succeeded
    succeeded = []
    for task in outstanding_tasks:
        old_state, new_state, ready = task.update_state()

        if new_state in success_states:
            succeeded.append(task)

    return succeeded
