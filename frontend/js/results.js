import { get_poll_id } from "./utils.js";

const poll_id = get_poll_id();
var result_list = document.getElementById('results');
var poll_name = document.getElementById('poll-title');
var poll_winner = document.getElementById('poll-winner');
var poll_id_p = document.getElementById('poll-id');
var poll_date = document.getElementById('poll-date');
var poll_end = document.getElementById('poll-end');

document.addEventListener("DOMContentLoaded", fetchPoll);

async function fetchPoll(){
    const url = `/api/polls/${poll_id}/result`;
    try {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error(`Response status ${resp.status}`);
        }

        const result = await resp.json();
        console.log(result)
        poll_winner.textContent = `Winner is: ${result.winner}`;
        poll_name.textContent = `Poll: ${result.name} `;
        poll_id_p.textContent = `Poll id: ${poll_id}`;
        poll_date.textContent = `Poll created at: ${result.created_at}`;
        poll_end.textContent = `Poll closed at: ${result.closes_at}`;

        const rounds = result.rounds;
        make_results(rounds);

    } catch (error) {
        console.error(error.message);
    }
}

function make_results(rounds) {
    for (const [idx, round] of rounds.entries()) {
        var rondo_det = document.createElement('details');
        var rondo_number = document.createElement('summary');
        rondo_number.textContent = `Round ${idx+1}`;
        rondo_det.appendChild(rondo_number);
        for (const opt of round) { 
            var option = document.createElement('div');
            console.log(opt);
            option.id = opt.id;
            option.className = "result-card";
            option.textContent = 
                `${opt.option} ${opt.votes} ${opt.status}`;
            rondo_det.appendChild(option);
        }
        result_list.appendChild(rondo_det);
    }
}
