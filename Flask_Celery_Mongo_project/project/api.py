from celery import group, chain, chord
from flask import (
    Flask,
    request,
    url_for,
    jsonify,
    Blueprint,
)

from project.tasks import add, long_task, tsum
from project.models import User, Status

celery_blueprint = Blueprint(
    "celery", __name__, url_prefix="/celery_tasks"
)


@celery_blueprint.route("/chaintask", methods=["GET"])
def run_celery_chain_task_example():
    pass_result = request.args.get("pass_result")
    if pass_result:
        result = chain(add.s(2, 2), add.s(4), add.s(8))()
    else:
        result = chain(add.si(2, 2), add.si(4, 4), add.si(8, 8))()
    output = {"Status": "SUCCESS", "Result": result.get()}
    return jsonify(output), 202, output


@celery_blueprint.route("/grouptask", methods=["GET"])
def run_celery_group_task_example_2():
    res = group(add.s(i, i) for i in range(10))()
    output = {"Status": "SUCCESS", "Result": res.get()}
    return jsonify(output), 202, output


@celery_blueprint.route("/chordtask", methods=["GET"])
def run_celery_chord_task_example():
    res = chord(add.s(i, i) for i in range(10))(tsum.s())
    output = {"Status": "SUCCESS", "Result": res.get()}
    return jsonify(output), 202, output


@celery_blueprint.route("/longtask", methods=["POST"])
def longtask():
    group_task = request.args.get("group_task")
    task = long_task.apply_async(args=[group_task])
    response = {
        "output":{
            "task":task.id,
            "task_url":url_for(
                "celery.check_task",task_id=task.id, _external=True
            )
        }
    }
    return jsonify(response), 202, response


@celery_blueprint.route('/status/<task_id>')
def check_task(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
