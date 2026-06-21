import sqlite3

from datetime import datetime, timezone

from flask import (
    Flask, session,
    request, jsonify,
    Blueprint, current_app
)

from voxpopulli.db import get_db

bp = Blueprint('poll', __name__, url_prefix='/api')

@bp.route("/poll", methods=['GET'])
def get_latest_poll():
    stmt = ( 
        "SELECT poll_id, name, created_at, closes_at from polls "
        " ORDER BY created_at DESC LIMIT 1;"
    )
    db = get_db()
    row = db.execute(stmt).fetchone()
    name = row['name']
    poll_id = row['poll_id']
    poll_start = row['created_at']
    poll_end = row['closes_at']
    options = get_suggestions(poll_id)

    resp_dic = {
        'name': name,
        'id': poll_id,
        'options': options,
        'start': poll_start,
        'end': poll_end
    }

    return jsonify(resp_dic)

@bp.route("/poll/<poll_id>", methods=['GET'])
def get_poll(poll_id):
    stmt = ( 
        "SELECT poll_id, name, created_at, closes_at from polls "
        " WHERE poll_id = ?;"
    )
    db = get_db()
    row = db.execute(stmt, (poll_id, )).fetchone()
    name = row['name']
    poll_start = row['created_at']
    poll_end = row['closes_at']

    options = get_suggestions(poll_id)

    poll = {
        'name': name,
        'id': poll_id,
        'options': options,
        'start': poll_start,
        'end': poll_end
    }
        
    return jsonify(poll)

def get_suggestions(poll_id):
    db = get_db()
    sug_stmt = (
        "SELECT suggestion_id, text FROM suggestions "
        "WHERE poll_id == ?;"
    )
    rows = db.execute(sug_stmt, (poll_id, )).fetchall()
    options = []
    for r in rows:
        opt = {
            'text': r['text'],
            'id': r['suggestion_id']
        }
        options.append(opt)

    return options

@bp.route("/poll/<poll_id>/ballot", methods=['GET'])
def get_ballot(poll_id):
    db = get_db()
    
    voter = session['voter_id']
    
    repl = (voter, poll_id)
    ballot_stmt = (
        "SELECT b.submited_at, s.text, r.ranked "
        "FROM ballots b "
        "INNER JOIN rankings r on r.ballot_id = b.ballot_id "
        "INNER JOIN suggestions s on r.suggestion_id = s.suggestion_id "
        "WHERE b.voter_id = ? AND b.poll_id = ?;"
    )
    rows = db.execute(ballot_stmt, repl).fetchall()
    ballot = []
    for row in rows:
        rank = row['ranked']
        text = row['text']
        submitted = row['submited_at']
        ballot.append(dict(row))

    print(ballot)
    response = { 
        'ranking' : ballot
    }

    return jsonify(response)


@bp.route("/poll/<poll_id>/ballot", methods=['POST'])
def cast_ballot(poll_id):
    ballot = request.get_json()
    ranking = ballot['ranking']
    ballot_stmt = (
        "INSERT INTO ballots (poll_id, submited_at, voter_id) "
        "VALUES (?, ?, ?) "
        "RETURNING ballot_id;"
    )

    voter_id = get_voter_id();
    if not voter_id:
        return {"Error": "Not authorized please login"}, 403

    current_date = datetime.now(timezone.utc)
    repl = (poll_id, current_date.isoformat(), voter_id)

    rank_stmt = (
        "INSERT INTO rankings (suggestion_id, ballot_id, ranked) "
        "VALUES (?, ?, ?);"
    )

    db = get_db()
    try:
        row = db.execute(ballot_stmt, repl).fetchone()
        ballot_id = row['ballot_id']
        params = []
        for rank, opt_id in enumerate(ranking):
            repl = (opt_id, ballot_id, rank)
            params.append(repl)
        db.executemany(rank_stmt, params)
        db.commit()
    except sqlite3.IntegrityError as e:
        # print(e)
        db.rollback()
        return {"Error": "ballot malformed"}, 409
        
    resp = {
        'id': ballot_id,
        'ranking': len(ranking)
    }
    return jsonify(resp)

def get_voter_id():
    voter = None
    if current_app.config.get('AUTH_MODE') == 'guest':
        voter = request.remote_addr
    else:
        voter = session.get('voter_id')
    return voter
