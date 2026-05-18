from flask import (
    Flask, session,
    Flask, redirect, request, session,
    Blueprint, current_app 
)

bp = Blueprint('poll', __name__)

@bp.route("/poll/<poll_id>", methods=['GET'])
def get_poll(poll_id):
    print(poll_id)
    return

@bp.route("/poll/<poll_id>", methods=['POST'])
def cast_ballot(poll_id):
    ballot = request.get_json()
    return
