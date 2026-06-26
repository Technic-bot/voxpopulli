import { get_poll_id } from "./utils.js";

const poll_id = get_poll_id();
var result_list = document.getElementById('results');
// var poll_name = document.getElementById('poll-title');
var poll_winner = document.getElementById('poll-winner');
// var poll_id_p = document.getElementById('poll-id');
// var poll_date = document.getElementById('poll-date');
// var poll_end = document.getElementById('poll-end');

document.addEventListener("DOMContentLoaded", fetchPoll);

async function fetchPoll(){
    const url = `/api/poll/${poll_id}/result`;
    try {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error(`Response status ${resp.status}`);
        }

        const result = await resp.json();
        poll_winner.textContent = result.winner;
        const rounds = result.rounds;
        rounds.forEach(make_results);

    } catch (error) {
        console.error(error.message);
    }
}

function make_results(round) {
    var rondo = document.createElement('div');
    for (const opt of round) { 
        var option = document.createElement('div');
        console.log(opt);
        option.id = opt.id;
        option.className = "result";
        option.textContent = 
            `${opt.option} ${opt.votes} ${opt.status}`;
        rondo.appendChild(option);

    }
    result_list.appendChild(rondo);
}
