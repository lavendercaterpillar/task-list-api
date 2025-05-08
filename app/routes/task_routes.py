from flask import Blueprint, Response, make_response, request, jsonify
from app.models.task import Task
from ..db import db
from .helper import validate_model, create_model
from datetime import datetime
import os
import requests

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    model_dict, status = create_model(Task, request_body)
    return {"task": model_dict}, status

@bp.get("")
def get_all_tasks():

    query = db.select(Task)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify({"task":task.to_dict()})


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update_from_dict(request_body)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    # Slack chat:write Arguements
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = "C08NTC26TM1"
    slack_message = {
        "channel": slack_channel,
        "text": f"Someone just completed the task My Beautiful Task"
    }

    # Slack API headers by requests
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    # Send message to Slack
    requests.post("https://slack.com/api/chat.postMessage", json=slack_message, headers=headers)    
    return Response(status=204, mimetype="application/json")


# @bp.patch("/<task_id>/mark_complete")
# def mark_complete(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = datetime.now()
#     db.session.commit()
#     return Response(status=204, mimetype="application/json")


@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")