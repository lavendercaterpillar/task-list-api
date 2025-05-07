from flask import Blueprint, Response, make_response, request  # additional imports for refactoring option 2
from app.models.task import Task
from ..db import db
from .helper import validate_model

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    # lines 18 and 19 are responsible for saving the new task to the database.
    db.session.add(new_task) 
    db.session.commit() 

    # We need to convert response body back to JSON
    response = new_task.to_dict()
    return response, 201