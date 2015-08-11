# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import logging

from threedi_task.models import Task


logger = logging.getLogger(__name__)

# see Celery source
SUCCESS_STATES = ['SUCCESS']
FAILURE_STATES = ['FAILURE', 'REVOKED']
READY_STATES = SUCCESS_STATES + FAILURE_STATES


def update_and_get_succeeded(
        task_name=None, success_states=SUCCESS_STATES,
        failure_states=FAILURE_STATES, method='async_result',
        djcelery_api_url='', *args, **kwargs):
    """
    Check the state of the tasks and update it via Celery.

    Params:
        task_name: a specific task name to update, if None: update all tasks
        success_states: states which count as success
        failure_states: states which count as failed (will be excluded)
        method:
            - async_result: use Celery AsyncResult to update the state
            - djcelery_api: use a call to the djcelery api to update the state
        djcelery_api_url: the api base url for method='djcelery_api'
    Returns:
        a list of succeeded tasks
    """
    if method == 'djcelery_api' and not djcelery_api_url:
        raise Exception("No Djcelery API url given for method="
                        "djcelery_api")

    # First get all the outstanding tasks from the db
    tasks = Task.objects.filter(name=task_name) if task_name else \
        Task.objects.all()
    outstanding_tasks = tasks.exclude(state__in=READY_STATES)

    # Check if the outstanding tasks have succeeded
    succeeded = []
    for task in outstanding_tasks:
        if method == 'async_result':
            updated_state = task.update_state_async_result()
        elif method == 'djcelery_api':
            try:
                updated_state = task.update_state_djcelery_api(
                    djcelery_api_url)
            except Exception, e:
                print(e)
                logger.error(e)
                continue

        if updated_state.new_state in success_states:
            succeeded.append(task)

    return succeeded
