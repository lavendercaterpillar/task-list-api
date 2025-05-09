from flask import Blueprint, Response, abort, make_response, request, jsonify
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from .helper import validate_model, create_model

bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    model_dict, status = create_model(Goal, request_body)
    return {"goal": model_dict}, status

# My implementation
# @bp.post("/<goal_id>/tasks")
# def create_task_with_goal(goal_id):
#     goal = validate_model(Goal, goal_id)
    
#     request_body = request.get_json()
#     request_body["goal_id"] = goal.id

#     try:
#         new_task = Task.from_dict(request_body)

#     except KeyError as error:
#         response = {"message": f"Invalid request: missing {error.args[0]}"}
#         abort(make_response(response, 400))
        
#     db.session.add(new_task)
#     db.session.commit()

#     response = new_task.to_dict()
#     return jsonify({"task": response}), 201


# Sending a list of Task IDs to Goal  GPT
# @bp.route('/<goal_id>/tasks', methods=['POST'])
# def assign_tasks_to_goal(goal_id):
#     # Validate the goal exists
#     goal = validate_model(Goal, goal_id)

#     # Get and validate request body
#     request_body = request.get_json()


#     task_ids = request_body["task_ids"]
    
#     # Validate each task_id exists and update its goal_id
#     updated_task_ids = []
#     for task_id in task_ids:
#         task = validate_model(Task, task_id)
#         task.goal_id = goal.id
#         updated_task_ids.append(task_id)

#     db.session.commit()

#     # Return the response in the exact format expected by tests
#     return jsonify({
#         "id": goal.id,
#         "task_ids": updated_task_ids
#     }), 200

@bp.route('/<goal_id>/tasks', methods=['POST'])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_ids = request.get_json().get("task_ids", [])

    goal.tasks = [validate_model(Task, task_id) for task_id in task_ids]

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200

@bp.get("/<goal_id>/tasks")
def read_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        task_dict = {
            "id": task.id,
            "goal_id": goal.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
        tasks_response.append(task_dict)

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response  
    }

    return jsonify(response_body), 200


@bp.get("")
def get_all_goals():

    query = db.select(Goal)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Goal.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Goal.title.desc())
    else:
        query = query.order_by(Goal.id)

    goals = db.session.scalars(query)
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return goals_response


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({"goal":goal.to_dict()})


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.update_from_dict(request_body)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")