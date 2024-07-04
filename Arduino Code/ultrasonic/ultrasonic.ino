// Pin definitions
const int enA = 3;  // Enable pin for motor A
const int in1 = 4;  // Control pin 1 for motor A
const int in2 = 7;  // Control pin 2 for motor A
const int trigPin = 8; // Trigger pin for ultrasonic sensor
const int echoPin = 9; // Echo pin for ultrasonic sensor

void setup() {
  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  // Set the ultrasonic sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Set motor direction forward
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);

  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  // Start the motor
  analogWrite(enA, 200); // Set motor speed to desired value (200)

  // Check the distance from the ultrasonic sensor
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1; // Convert duration to distance in cm

  Serial.print("Distance: ");
  Serial.println(distance); // Print the distance for debugging

  // Stop the motor if an object is detected within 10 cm
  if (distance <= 10) {
    analogWrite(enA, 0); // Stop the motor
  }

  // Pause for a short time before the next loop iteration
  delay(100);
}