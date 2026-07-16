import {get_poll_id} from './utils.js';

var polls_div = document.getElementById('polls');
var next_button = document.getElementById('next-button');

document.addEventListener("DOMContentLoaded", fetchPolls);

async function fetchPolls(){
    const urlParams = new URLSearchParams(window.location.search);
    const offset = urlParams.get('offset') || '0' ;
    const limit = urlParams.get('limit') || '10' ;

    const url = `api/polls?offset=${offset}&limit=${limit}`;
    try {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error(`Response status ${resp.status}`);
        }

        const polls = await resp.json();
        console.log(polls);
        make_polls(polls);

    } catch (error) {
        console.error(error.message);
    }
}

function make_polls(polls) {
    for (const p of polls) {
        var poll_el = document.createElement('div');
        var poll_url = document.createElement('a');
        const poll_id = p.poll_id;
        poll_el.className = 'poll';
        poll_el.id = poll_id;
        poll_url.href = `poll?id=${poll_id}`;
        poll_url.textContent = p.name + " " + p.closes_at;
        poll_el.appendChild(poll_url);
        polls_div.appendChild(poll_el);
    }
}

