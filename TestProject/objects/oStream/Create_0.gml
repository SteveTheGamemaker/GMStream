// Initialize socket variables
global.socket = -1;
global.host = ""; // Replace with your IP (SOCKET_HOST in the .env)
global.port = 8080; // Replace with your socket port (SOCKET_PORT in the .env)
global.connected = false;

// Attempt to connect to the socket server
global.socket = network_create_socket(network_socket_tcp);

// Check if socket creation was successful
if (global.socket != -1) {
    var connection = network_connect_raw(global.socket, global.host, global.port);
    if (connection != -1) {
        global.connected = true;
        show_debug_message("Successfully connected to the server.");
    } else {
        show_debug_message("Failed to connect to the server.");
    }
} else {
    show_debug_message("Failed to create a socket.");
}