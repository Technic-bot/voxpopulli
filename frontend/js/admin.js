const admin_submit = document.getElementById('submit-poll');
admin_submit.addEventListener("click", submit_poll);

const suggestions = document.getElementById('suggestions');
suggestions.addEventListener("drop", process_drop);
suggestions.addEventListener("dragover", enable_drag);

const file_selector = document.getElementById('file-selector');
file_selector.addEventListener("change", process_select);

const poll_name = document.getElementById('poll-name');
const end_date = document.getElementById('end-date');
const poll_id = document.getElementById('poll-id');

async function submit_poll() {
    const txt = suggestions.value;
    const suggs = txt.split("\n");
    const payload = {
        'name' : poll_name.value,
        'closes_at' : end_date.value,
        'suggestions' : suggs
    }
    const url = '/api/admin/poll';
    try {
        const resp = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        console.log(payload);
        if (!resp.ok) {
            throw new Error(`Response status ${response.status}`);
        }

        const result = await resp.json();
        const published_id = result.id;
        poll_id.textContent = `Poll: ${published_id} published`;
    } catch (error) {
        console.error(error.message);
    }
}

function enable_drag(e) {
    e.preventDefault();
}

function process_drop(e) {
    const files = e.dataTransfer.files;
    process_options(files);
}

function process_select(e) {
    console.log('elected');
    const files = e.target.files;
    process_options(files);
} 

function process_options(files) {
    console.log(files);
    if (files) {
        const file = files[0];
        const reader = new FileReader();
        reader.onload = () => {
            suggestions.value = reader.result;
        }
        reader.readAsText(file);
    }
}
