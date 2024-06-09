import threading

import cv2
import numpy as np
import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from pyzbar.pyzbar import decode

app = Flask(__name__)
socketio = SocketIO(app)

# Store detected QR codes
detected_qr_codes = []

@app.route('/')
def index():
    return render_template('index.html', qr_codes=detected_qr_codes)

@app.route('/submit_qr_code', methods=['POST'])
def submit_qr_code():
    data = request.form['data']
    if data not in detected_qr_codes:
        detected_qr_codes.append(data)
        socketio.emit('new_qr_code', data)  # Emit event to notify clients
    return 'OK', 200

def send_qr_code_to_server(data):
    url = 'http://localhost:5000/submit_qr_code'
    response = requests.post(url, data={'data': data})
    if response.status_code == 200:
        print("Data sent to server successfully.")
    else:
        print("Failed to send data to server.")

def scan_qr_codes():
    # Open the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    detected_qr_codes_set = set()

    while True:
        # Read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Decode the QR code in the frame
        decoded_objects = decode(frame)
        
        for obj in decoded_objects:
            # Extract the QR code data
            qr_data = obj.data.decode('utf-8')
            
            # Check if the QR code has already been detected
            if qr_data in detected_qr_codes_set:
                continue  # Skip already detected QR codes
            
            # Add the QR code data to the set
            detected_qr_codes_set.add(qr_data)
            
            # Print the data
            print(f"Data: {qr_data}")
            
            # Send the QR code data to the server
            send_qr_code_to_server(qr_data)
        
        # Display the frame with a rectangle around the detected QR code
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4: 
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points
            
            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j+1) % n], (0, 255, 0), 3)
        
        cv2.imshow('QR Code Scanner', frame)
        
        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Start the QR code scanning in a separate thread
    threading.Thread(target=scan_qr_codes).start()
    # Start the Flask server with SocketIO
    socketio.run(app, debug=True)
