
import cv2
import numpy as np
import serial
import time
from pyzbar.pyzbar import decode

# Initialize serial communication with Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)  # Ensure 'COM5' is the correct port
time.sleep(2)  # Wait for the serial connection to initialize

# Function to rotate the motor
def rotate_motor(command):
    if arduino:
        try:
            arduino.write(command.encode())  # Send command to Arduino
            print(f"Motor rotation command '{command}' sent to Arduino")
        except Exception as e:
            print("Error sending command to Arduino:", e)
    else:
        print("Arduino not initialized. Motor control not possible.")

# Function to scan QR codes
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
            
            # Rotate motor to 180 degrees
            rotate_motor('R')
            time.sleep(5)  # Wait for 5 seconds
            # Rotate motor back to 0 degrees
            rotate_motor('O')
        
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
    arduino.close()

if __name__ == '__main__':
    scan_qr_codes()
