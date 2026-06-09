var options = document.getElementById('options'),
    choices = document.getElementById('choices');

console.log(options);
console.log(choices);

const opts_sortable = new Sortable(options, {
    group: 'shared',
    animation: 150
});

const choi_sortable = new Sortable(choices, {
    group: 'shared',
    animation: 150
});

console.log(choi_sortable.toArray())

document.addEventListener("DOMContentLoaded", fetchLatestPoll);

async function fetchLatestPoll(){
    const url = "/api/poll";
    try {
        const resp = await fetch(url);
        if (!resp.ok) {
            throw new Error(`Response status ${response.status}`);
        }

        const result = await response.json();
        console.log(result);
    } catch (error) {
        console.error(error.message);
    }
}


