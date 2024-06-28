from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
from pyzbar.pyzbar import decode
import cv2
import requests

app = Flask(__name__)
socketio = SocketIO(app)

detected_qr_codes_set = set()

def send_qr_code_to_server(data):
    url = 'http://localhost:5000/submit_qr_code'
    requests.post(url, data={'data': data})

def scan_qr_codes():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            if qr_data in detected_qr_codes_set:
                continue
            detected_qr_codes_set.add(qr_data)
            send_qr_code_to_server(qr_data)
            socketio.emit('new_qr_code', qr_data)
        socketio.emit('detected_qr_codes', list(detected_qr_codes_set))
        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_qr_code', methods=['POST'])
def submit_qr_code():
    data = request.form['data']
    if data not in detected_qr_codes_set:
        detected_qr_codes_set.add(data)
        socketio.emit('new_qr_code', data)
    return 'OK', 200

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

if __name__ == '__main__':
    threading.Thread(target=scan_qr_codes).start()
    socketio.run(app, debug=True)
