import cv2
import zbarlight
import json
import openpyxl
from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)

excel_file = 'qr_code_data.xlsx'
excel_columns = [
    "product_id", "product_name", "category", "date_of_manufacture", "expiry_date", 
    "batch_number", "batch_size", "source_location", "certification", 
    "stock_level", "order_id", "customer_id", "timestamp"
]

def update_excel(data):
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active
    row = [data[col] for col in excel_columns]
    sheet.append(row)
    workbook.save(excel_file)

def scan_qr_codes():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qr_codes = zbarlight.scan_codes('qrcode', gray)
        if qr_codes:
            for qr_code in qr_codes:
                qr_data = qr_code.decode('utf-8')
                try:
                    data = eval(qr_data)
                    if isinstance(data, dict):
                        update_excel(data)
                        socketio.emit('new_qr_code', data)
                except Exception as e:
                    print(f"Failed to decode QR code data: {e}")
        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/qr_code_data.xlsx')
def download_excel():
    return send_from_directory('', excel_file)

if __name__ == "__main__":
    thread = threading.Thread(target=scan_qr_codes)
    thread.start()
    socketio.run(app)

