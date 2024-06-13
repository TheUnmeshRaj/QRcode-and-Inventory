#include <Servo.h>

Servo myServo; 
int servoPin = 9;

void setup() {
  myServo.attach(servoPin);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'R') {
      myServo.write(180);
    } else if (command == 'O') {
      myServo.write(0); 
    }
  }
}
