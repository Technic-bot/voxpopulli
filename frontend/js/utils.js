export function get_poll_id(){
    // Gets the poll requested via url if applicable
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    var poll_id = "";
    if (id) {
        poll_id = "/" + id;
    }
    return poll_id;
}
