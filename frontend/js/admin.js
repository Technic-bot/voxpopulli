const admin_submit = document.getElementById('submit-poll');
admin_submit.addEventListener("click", submit_poll);

const suggestions = document.getElementById('suggestions');
suggestions.addEventListener("drop", process_drop);
suggestions.addEventListener("dragover", enable_drag);

const file_selector = document.getElementById('file-selector');
file_selector.addEventListener("change", process_select);


function submit_poll() {
    console.log(this.classname);
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
