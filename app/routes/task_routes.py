from flask import Blueprint, Response, make_response, request, jsonify
from app.models.task import Task
from ..db import db
from .helper import validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task) 
    db.session.commit() 

    return jsonify({"task": new_task.to_dict()}), 201

@tasks_bp.get("")
def get_all_tasks():

    query = db.select(Task)

    # title_param = request.args.get("title")
    # if title_param:
    #     query = query.where(Task.title.ilike(f"%{title_param}%"))

    # description_param = request.args.get("description")
    # if description_param:
    #     query = query.where(Task.description.ilike(f"%{description_param}%"))

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict()


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update_from_dict(request_body)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")