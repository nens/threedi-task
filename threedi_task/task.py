# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import logging

from threedi_task.models import Task


logger = logging.getLogger(__name__)

SUCCESS_STATES = ['SUCCESS']
FAILURE_STATES = ['FAILURE']


def update_task_states(
        task_name=None, success_states=SUCCESS_STATES,
        failure_states=FAILURE_STATES, *args, **kwargs):
    """Check the state of the tasks and update it"""
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
            succeeded.append(task.uuid)

    return succeeded
