# GMStream GameMaker Live Stream Project

This project allows you to stream your GameMaker games visuals directly to a web browser using Flask and a socket server.

## Getting Started

Follow the steps below to set up and run the project.

### 1. Configure Environment Variables

Add your IP and two available ports to the `.env` file:

```plaintext
FLASK_HOST=Your_IP_Address       # IP used to host the Flask server
SOCKET_HOST=Your_IP_Address      # IP used to host the socket server for GameMaker
FLASK_PORT=Your_Flask_Port       # Port used to host the Flask server
SOCKET_PORT=Your_Socket_Port     # Port used to host the socket server
```

### 2. Understanding the Difference Between Flask and Socket Server

- **Socket Server:** This server is used to facilitate communication between GameMaker and `app.py`. GameMaker uses the socket on this port to send the raw pixel data from your game.
  
- **Flask Server:** This server is specifically used to deliver the frontend content that contains your game stream.

### 3. Add `oStream` to Your GameMaker Project

1. Add the `oStream` object to your GameMaker project.
2. Modify the create event of oStream to use your SOCKET_HOST and SOCKET_PORT
3. Add `oStream` to the first room in your game. It's persistent, so it will carry over between rooms.

### 4. Run the Servers

1. Launch the `app.py` script:

   ```bash
   python app.py
   ```

2. Launch your GameMaker game.

### 5. View Your Stream

1. Open your web browser.
2. Go to `FLASK_HOST:FLASK_PORT`.

You should see your GameMaker game being streamed in your browser!