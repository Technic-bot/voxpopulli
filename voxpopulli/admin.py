from flask import (
    Flask, session,
    Flask, redirect, request, session,
    Blueprint, current_app 
)

bp = Blueprint('admin', __name__, url_prefix='admin')

@bp.route("/admin")
def publish_poll():
    pass
