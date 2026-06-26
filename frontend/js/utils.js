export function get_poll_id(){
    // Gets the poll requested via url if applicable
    const path = window.location.pathname;
    var poll_id = "";
    if (path.startsWith("/poll/")) {
        poll_id = "/" + path.split("/")[2];
    }
    return poll_id;
}
