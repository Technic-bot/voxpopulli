var options = document.getElementById('options'),
    choices = document.getElementById('choices');

var poll_name = document.getElementById('poll-title');
var poll_date = document.getElementById('poll-date');
var poll_ends = document.getElementById('poll-ends');

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


        console.log(result);
    } catch (error) {
        console.error(error.message);
    }
}


