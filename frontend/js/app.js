var options = document.getElementById('options'),
    choices = document.getElementById('choices');

var poll_name = document.getElementById('poll-title');
var poll_date = document.getElementById('poll-date');
var poll_end = document.getElementById('poll-end');

var option_list = document.getElementById('options');

const opts_sortable = new Sortable(options, {
    group: 'shared',
    animation: 150
});

const choi_sortable = new Sortable(choices, {
    group: 'shared',
    animation: 150
});

console.log(choi_sortable.toArray())

document.addEventListener("DOMContentLoaded", fetchPoll);

async function fetchPoll(){
    const path = window.location.pathname;
    var poll_id = "";
    if (path.startsWith("/poll/")) {
        poll_id = "/" + path.split("/")[2];
    }

    const url = `/api/poll${poll_id}`;
    try {
        console.log(url);
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error(`Response status ${response.status}`);
        }

        const result = await resp.json();
        poll_name.textContent = result.name;
        poll_date.textContent = "Poll submitted at " + result.start;
        poll_end.textContent = "Poll closes at " + result.end;
        opts = result.options;
        opts.forEach(make_suggestions);

    } catch (error) {
        console.error(error.message);
    }
}

function make_suggestions(option) {
    var suggestion = document.createElement('div');
    suggestion.id = option.id;
    suggestion.className = "opt";
    suggestion.textContent = option.text;
    option_list.appendChild(suggestion);
}

