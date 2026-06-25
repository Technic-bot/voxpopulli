from datetime import datetime, timedelta, timezone

from flask import (
    Flask, session,
    request,
    Blueprint, jsonify
)

from voxpopulli.db import get_db

bp = Blueprint('admin', __name__, url_prefix="/api")

@bp.route("/admin/poll", methods=['POST'])
def publish_poll():
    poll = request.get_json()

    poll_stmt = (
        "INSERT INTO polls (name, created_at, closes_at) "
        "VALUES (?, ?, ?) "
        "RETURNING poll_id;" 
    )
    
    curr_time = datetime.now(timezone.utc)
    created_at = curr_time.isoformat()
    name = poll['name']
    closes_at = poll['closes_at']
    
    db = get_db()
    row = db.execute(poll_stmt, (name, created_at, closes_at)).fetchone()

    poll_id = row['poll_id']
    
    sug_params = []
    for s in poll['suggestions']:
        sug_text = s.strip()
        if sug_text:
            sug_params.append((poll_id, sug_text))

    sug_stmt = (
        "INSERT INTO suggestions (poll_id, text) "
        "VALUES (?, ?)"
    )
    db.executemany(sug_stmt, sug_params)
    db.commit()
        
    resp_dic = {
        'id': poll_id, 
        'suggestions': len(sug_params),
        'closing': closes_at
    }        

    return jsonify(resp_dic)

