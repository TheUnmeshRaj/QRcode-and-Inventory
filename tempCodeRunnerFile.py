import cv2
import numpy as np
import serial
import time
import threading
import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from pyzbar.pyzbar import decode

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize serial communication with Arduino
arduino = None

def init_serial(port, baud_rate=9600):
    global arduino
    try:
        arduino = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for serial connection to stabilize
        print(f"Arduino connected on port {port}")
    except serial.SerialException as e:
        print(f"Failed to connect to Arduino on port {port}: {e}")

# Function to rotate the motor
def rotate_motor(command):
    if arduino and arduino.is_open:
        try:
            arduino.write(command.encode())  # Send command to Arduino
            print(f"Motor rotation command '{command}' sent to Arduino")
        except Exception as e:
            print("Error sending command to Arduino:", e)
    else:
        print("Arduino not initialized or not connected. Motor control not possible.")

# Global variable to store detected QR codes
detected_qr_codes_set = set()

# Function to send QR code data to server
def send_qr_code_to_server(data):
    url = 'http://localhost:5000/submit_qr_code'
    response = requests.post(url, data={'data': data})
    if response.status_code == 200:
        print("Data sent to server successfully.")
    else:
        print("Failed to send data to server.")

# Function to scan QR codes
def scan_qr_codes():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        decoded_objects = decode(frame)
        
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            
            if qr_data in detected_qr_codes_set:
                continue
            
            detected_qr_codes_set.add(qr_data)
            
            print(f"Data: {qr_data}")
            
            # Rotate motor to 180 degrees
            rotate_motor('R')
            time.sleep(5)  # Wait for 5 seconds
            # Rotate motor back to 0 degrees
            rotate_motor('O')
            
            # Send QR code data to server
            send_qr_code_to_server(qr_data)
            
            # Emit new QR code to clients via SocketIO
            socketio.emit('new_qr_code', qr_data)  # Update clients with new QR code

        # Display detected QR codes in a web interface
        socketio.emit('detected_qr_codes', list(detected_qr_codes_set))

        # Draw polygons around detected QR codes
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            n = len(hull)
            for j in range(0, n):
                cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 3)

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    if arduino:
        arduino.close()

# Flask routes and SocketIO events
@app.route('/')
def index():
    return render_template('index.html', qr_codes=list(detected_qr_codes_set))

@app.route('/submit_qr_code', methods=['POST'])
def submit_qr_code():
    data = request.form['data']
    if data not in detected_qr_codes_set:
        detected_qr_codes_set.add(data)
        socketio.emit('new_qr_code', data)  
    return 'OK', 200

if __name__ == '__main__':
    init_serial('COM5')  # Replace 'COM5' with your Arduino port
    threading.Thread(target=scan_qr_codes).start()
    socketio.run(app, debug=True)
