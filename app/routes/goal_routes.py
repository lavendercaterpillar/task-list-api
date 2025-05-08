from flask import Blueprint, Response, make_response, request, jsonify
from app.models.goal import Goal
from ..db import db
from .helper import validate_model, create_model
# from datetime import datetime
# import os
# import requests

bp = Blueprint("goals", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    model_dict, status = create_model(Goal, request_body)
    return {"goal": model_dict}, status


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