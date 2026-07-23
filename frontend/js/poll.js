import {get_poll_id} from './utils.js';

var options = document.getElementById('options'),
    choices = document.getElementById('choices');

var poll_name = document.getElementById('poll-title');
var poll_id_p = document.getElementById('poll-id');
var poll_date = document.getElementById('poll-date');
var poll_end = document.getElementById('poll-end');

var option_list = document.getElementById('options');
var submit_button = document.getElementById('submit-button');

var ballot_state = document.getElementById('ballot-status');

const opts_sortable = new Sortable(options, {
    group: 'shared',
    animation: 150
});

const choi_sortable = new Sortable(choices, {
    group: 'shared',
    animation: 150
});

document.addEventListener("DOMContentLoaded", fetchPoll);
submit_button.addEventListener("click", submit_ballot);

async function fetchPoll(){
    const url = `api/polls${poll_id}`;
    try {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error(`Response status ${resp.status}`);
        }

        const result = await resp.json();
        poll_name.textContent = result.name;
        poll_date.textContent = "Poll submitted at " + result.created_at;
        poll_end.textContent = "Poll closes at " + result.closes_at;
        poll_id_p.textContent = "Poll id: " + result.id;
        poll_id = result.id;
        const opts = result.options;
        opts.forEach(make_suggestions);

    } catch (error) {
        console.error(error.message);
    }
}

var poll_id = get_poll_id();

function make_suggestions(option) {
    var suggestion = document.createElement('div');
    suggestion.id = option.id;
    suggestion.setAttribute('data-id',option.id);
    suggestion.className = "opt";
    suggestion.textContent = option.text;
    option_list.appendChild(suggestion);
}

async function submit_ballot(){
    const ranking = choi_sortable.toArray();
    const payload = {
        'ranking': ranking
    };
    try {
        const url = `api/polls/${poll_id}/ballot`;
        const resp = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        if (!resp.ok) {
            const error_msg = await resp.json();
            ballot_state.textContent = error_msg.message;
            throw new Error(`Response status ${resp.status}`);
        }
    } catch (error) {
        console.error(error.message);
    }
} 
