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
    suggestions = poll['suggestions']
    proc_suggs = parse_suggestions(suggestions)
    for s in proc_suggs:
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

def parse_suggestions(suggestions):
    """ 
        Remove whitespace and duplicates suggestions 
        A suggestion is duplicate even if casing vaires 
    """
    canon_sugs = []
    sug_set = set()
    for s in suggestions:
        no_white_space = s.strip()
        # No whitespace suggestions
        if not no_white_space:
            continue
        # Deduplicate
        lower_sug = no_white_space.lower()
        if not lower_sug in sug_set:
            sug_set.add(lower_sug) 
            canon_sugs.append(no_white_space)
    return canon_sugs
