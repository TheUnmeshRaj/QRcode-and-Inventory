import threading

import cv2
import numpy as np
import requests
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from pyzbar.pyzbar import decode

app = Flask(__name__)
socketio = SocketIO(app)

detected_qr_codes = []

@app.route('/')
def index():
    return render_template('index.html', qr_codes=detected_qr_codes)

@app.route('/submit_qr_code', methods=['POST'])
def submit_qr_code():
    data = request.form['data']
    if data not in detected_qr_codes:
        detected_qr_codes.append(data)
        socketio.emit('new_qr_code', data)  
    return 'OK', 200

def send_qr_code_to_server(data):
    url = 'http://localhost:5000/submit_qr_code'
    response = requests.post(url, data={'data': data})
    if response.status_code == 200:
        print("Data sent to server successfully.")
    else:
        print("Failed to send data to server.")

def scan_qr_codes():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    detected_qr_codes_set = set()

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
            
            send_qr_code_to_server(qr_data)
        
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
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=scan_qr_codes).start()
    socketio.run(app, debug=True)
