// new arduino code
const int enA = 3;  // Enable pin for motor A
const int in1 = 4;  // Control pin 1 for motor A
const int in2 = 7;  // Control pin 2 for motor A

void setup() {
  // Set all the motor control pins to outputs
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  // Set motor direction forward
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
}

void loop() {
  // Start the motor
  analogWrite(enA, 200); // Set motor speed to desired value (200)

  // Run the motor for 1 second
  delay(400);

  // Stop the motor
  analogWrite(enA, 0);

  // Pause for 4 seconds
  delay(3000);
}