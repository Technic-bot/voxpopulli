from flask import (
    Flask, session,
    Flask, redirect, request, session,
    Blueprint, current_app 
)

from voxpopulli.db import get_db

bp = Blueprint('poll', __name__)

@bp.route("/poll", methods=['GET'])
def get_latest_poll():
    stmt = ( 
        "SELECT poll_id, name, created_at, closes_at from polls "
        " ORDER BY created_at DESC LIMIT 1;"
    )
    db = get_db()
    row = db.execute(stmt).fetchone()
    latest_name = row['name']

    return latest_name

@bp.route("/poll/<poll_id>", methods=['GET'])
def get_poll(poll_id):
    stmt = ( 
        "SELECT poll_id, name, created_at, closes_at from polls "
        " WHERE poll_id = ?;"
    )
    db = get_db()
    row = db.execute(stmt, (poll_id, )).fetchone()
    name = row['name']
    return name

@bp.route("/poll/<poll_id>", methods=['POST'])
def cast_ballot(poll_id):
    ballot = request.get_json()
    return
