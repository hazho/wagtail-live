class WebsocketsPublisher {
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.initialize_websocket_connection();
    }

    initialize_websocket_connection() {}
    initialize_on_message_event() {}
    initialize_on_error_event() {}

    start() {
        this.initialize_on_message_event();
        this.initialize_on_error_event();
    }
}

class GenericWebsocketsPublisher extends WebsocketsPublisher {
    initialize_websocket_connection() {
        this.websocket = new WebSocket(
            'ws://'
            + this.baseURL
            + '/ws/channel/'
            + channelID
            + '/'
        );
    }

    initialize_on_message_event() {
        this.websocket.onmessage = function (e) {
            process_updates(JSON.parse(e.data))
        };
    }

    initialize_on_error_event() {
        this.websocket.onclose = function(e) {
            console.error('Websocket closed unexpectedly.');
        };
    }
}
