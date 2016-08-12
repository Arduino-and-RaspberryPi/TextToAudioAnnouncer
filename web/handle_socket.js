var ws_port = 80;
var parts = document.URL.split(':');

if (parts.length >= 3)
    ws_port = parseInt(parts[parts.length - 1].replace("/", ""));

ws_port = (ws_port + 1).toString();

var server_url = ["ws:", parts[1], ":", ws_port, "/"].join("");
var websocket = new WebSocket(server_url);

websocket.onopen = function(evt) {
    console.log("Connected");
};

websocket.onclose = function(evt) {
    console.log("Disconnected");
};

websocket.onmessage = function(evt) {
    console.log(evt.data);
};

websocket.onerror = function(evt) {
    console.log("Shit happened");
    websocket.close();
};

function sendMessage(message) {
    websocket.send(message);
}
