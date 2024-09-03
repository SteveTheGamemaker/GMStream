from flask import Flask, Response
import cv2
import numpy as np
import threading
import socket
import os
from dotenv import load_dotenv

app = Flask(__name__)

frame = None

load_dotenv()

# Get environment variables for IP and ports
FLASK_HOST = os.environ.get('FLASK_HOST')
FLASK_PORT = os.environ.get('FLASK_PORT')
SOCKET_HOST = os.environ.get('SOCKET_HOST')
SOCKET_PORT = os.environ.get('SOCKET_PORT')

# Ensure the SOCKET_PORT is converted to an integer
try:
    SOCKET_PORT = int(SOCKET_PORT)
except ValueError:
    raise ValueError(f"Invalid SOCKET_PORT: {SOCKET_PORT}. It must be an integer.")

@app.route('/video_feed')
def video_feed():
    def generate():
        global frame
        while True:
            if frame is not None:
                # Encode the frame in JPEG format
                _, jpeg = cv2.imencode('.jpg', frame)
                # Convert the frame to bytes
                frame_bytes = jpeg.tobytes()
                # Yield the frame in the format needed for MJPEG streaming
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
        <html>
            <head>
                <title>Video Streaming</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f0f0f0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                    }
                    .container {
                        text-align: center;
                        background: #fff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    h1 {
                        color: #333;
                    }
                    img {
                        border: 5px solid #ddd;
                        border-radius: 10px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Video Streaming</h1>
                    <img src="/video_feed" width="640" height="480">
                </div>
            </body>
        </html>
    '''

def run_socket_server():
    global frame
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to address and port
    server_socket.bind((SOCKET_HOST, SOCKET_PORT))
    # Enable the server to accept connections
    server_socket.listen(5)
    print(f"Socket server listening on port {SOCKET_PORT}")

    while True:
        # Establish connection with client
        client_socket, addr = server_socket.accept()
        print(f"Got connection from {addr}")

        try:
            while True:
                # Read the header first (12 bytes)
                header = client_socket.recv(12)
                if len(header) < 12:
                    break

                buffer_size = int.from_bytes(header[0:4], byteorder='little')
                target_width = int.from_bytes(header[4:8], byteorder='little')
                target_height = int.from_bytes(header[8:12], byteorder='little')

                # Read the actual buffer
                data = b''
                while len(data) < buffer_size:
                    packet = client_socket.recv(buffer_size - len(data))
                    if not packet:
                        break
                    data += packet

                if len(data) < buffer_size:
                    break

                # Convert data to numpy array and reshape to image
                frame = np.frombuffer(data, dtype=np.uint8).reshape((target_height, target_width, 4))
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Connection error: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {addr} closed")

if __name__ == '__main__':
    # Start the socket server in a new thread
    socket_thread = threading.Thread(target=run_socket_server)
    socket_thread.start()

    # Start the Flask app
    app.run(debug=False, host=FLASK_HOST, port=FLASK_PORT)