import sqlite3

from datetime import datetime, timezone

from flask import (
    Flask, session,
    request, jsonify,
    Blueprint, current_app
)

import pyrankvote
from pyrankvote import Candidate, Ballot

from voxpopulli.db import get_db

bp = Blueprint('polls', __name__, url_prefix='/api')

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
        'created_at': poll_start,
        'closes_at': poll_end
    }

    return jsonify(resp_dic)

@bp.route("/polls", methods=["GET"])
def get_polls():
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    stmt = ( 
        "SELECT poll_id, name, created_at, closes_at from polls "
        "ORDER BY created_at DESC LIMIT ? OFFSET ?;"
    )
    db = get_db()
    rows = db.execute(stmt, (limit,offset,)).fetchall()
    polls = []
    for r in rows:
        poll = {
            'name' : r['name'],
            'poll_id' : r['poll_id'],
            'created_at' : r['created_at'],
            'closes_at' : r['closes_at']
        }
        polls.append(poll)
    
    return polls


@bp.route("/polls/<poll_id>", methods=['GET'])
def get_poll(poll_id):
    poll = find_poll(poll_id)
    return jsonify(poll)


def find_poll(poll_id):
    stmt = ( 
        "SELECT poll_id, name, created_at, closes_at from polls "
        " WHERE poll_id = ?;"
    )
    db = get_db()
    row = db.execute(stmt, (poll_id, )).fetchone()
    poll = {}
    if row: 
        name = row['name']
        poll_start = row['created_at']
        poll_end = row['closes_at']

        options = get_suggestions(poll_id)

        poll = {
            'name': name,
            'id': poll_id,
            'options': options,
            'created_at': poll_start,
            'closes_at': poll_end
        }
    return poll
        

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

@bp.route("/polls/<poll_id>/ballot", methods=['GET'])
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

    response = { 
        'ranking' : ballot
    }

    return jsonify(response)


@bp.route("/polls/<poll_id>/ballot", methods=['POST'])
def cast_ballot(poll_id):
    poll = find_poll(poll_id)
    error, code = check_poll_accessible(poll);
    if error:
        return error, code
    
    if not check_poll_open(poll):
        error = {
            'error' : 'poll_finished',
            'message': 'Poll is closed cannot vote'
        }
        return error, 403

    voter_id = get_voter_id();
    if not voter_id:
        error = {
            'error' : 'unauthorized',
            'message': 'Not authorized please login'
        }
        return error, 403

    ballot = request.get_json()
    ranking = ballot['ranking']
    ballot_stmt = (
        "INSERT INTO ballots (poll_id, submited_at, voter_id) "
        "VALUES (?, ?, ?) "
        "RETURNING ballot_id;"
    )

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
        error = {
            'error' : 'double_vote',
            'message': f'Vote from {voter_id} already casted'
        }
        return {"Error": "ballot malformed"}, 409
        
    resp = {
        'id': ballot_id,
        'ranking': len(ranking)
    }
    return jsonify(resp)

def get_voter_id():
    voter = None
    if current_app.config.get('AUTH_MODE') == 'guest':
        voter = request.headers.get('X-Forwarded-For')
    else:
        voter = session.get('voter_id')
    return voter

def check_poll_accessible(poll):
    """ Check if poll exist and is accsible """
    error_json = None
    error_code = 200
    if not poll:
        error_json = {
            "error": "poll_not_found",
            "message" : "Poll does not exit"
        }
        error_code = 404
        
    return error_json, error_code

@bp.route("/polls/<poll_id>/result", methods=['GET'])
def get_poll_result(poll_id):
    poll = find_poll(poll_id)
    error, code = check_poll_accessible(poll);
    if error:
        return error, code
    
    if check_poll_open(poll):
        error = {
            'error' : 'poll_not_finished',
            'message': 'Poll is not closed'
        }
        return error, 403

    result_stmt = (
        "SELECT "
           "r.suggestion_id AS sugg_id, "
           "r.ballot_id AS ballot_id, "
           "b.poll_id AS poll_id, "
           "s.text AS text, "
           "r.ranked AS ranked FROM rankings r "
        "INNER JOIN ballots b ON b.ballot_id=r.ballot_id "
        "INNER JOIN suggestions s ON s.suggestion_id=r.suggestion_id "
        "WHERE b.poll_id=? "
        "ORDER BY r.ballot_id, r.ranked;"
    )

    db = get_db()
    rows = db.execute(result_stmt, (poll_id,)).fetchall()
    ballots = {}
    for r in rows:
        ballot_id = r['ballot_id']
        suggestion = r['text']
        if not ballot_id in ballots:
            suggs = [suggestion]
            ballots[ballot_id] = suggs
        else:
            ballots[ballot_id].append(suggestion)

    # Pass dict to pyRankVote here 
    result = instant_run_off(ballots)
    winner, rounds = decode_election(result)

    winners = {
        'name': poll['name'],
        'closes_at' : poll['closes_at'],
        'created_at' : poll['created_at'],
        'winner': winner,
        'rounds': rounds
    }

    return winners

def check_poll_open(poll):
    is_poll_open = True
    close_time = datetime.fromisoformat(poll['closes_at'], )
    if close_time < datetime.now():
        is_poll_open = False

    return is_poll_open

def instant_run_off(ballots):
    election_ballots = []
    election_candidates = []
    for b_id, suggs in ballots.items(): 
        pyrank_candidates = [] 
        for s in suggs:
            candidate = Candidate(s)
            election_candidates.append(candidate)
            pyrank_candidates.append(candidate)
        pyrank_ballot = Ballot(ranked_candidates=pyrank_candidates)
        election_ballots.append(pyrank_ballot)

    # Dedupplicating should not be needed per internal library workings 
    # But done for sanity
    election_candidates = list(set(election_candidates))
    result = pyrankvote.instant_runoff_voting(
        election_candidates,
        election_ballots)
    return result

def decode_election(result):
    winners = result.get_winners()
    if not winners:
        return []

    winner = winners[0].name
    pyrank_rounds = result.rounds
    rounds = []

    for r in pyrank_rounds:
        opt_result = []
        for pyround in r.candidate_results:
            candidate, votes, status = pyround
            suggestion = str(candidate)
            opt = {
                'option': suggestion,
                'votes': votes,
                'status': status
            }
            opt_result.append(opt)
        rounds.append(opt_result)
        
    return winner, rounds
