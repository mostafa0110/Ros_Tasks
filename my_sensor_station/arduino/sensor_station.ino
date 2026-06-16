/*
  Arduino sketch for Sensor Monitoring Station
  
  Hardware:
    HC-SR04: Trig -> Pin 9, Echo -> Pin 10
    Potentiometer: Middle pin -> A0
  
  Output (Serial at 9600 baud):
    "distance_cm,pot_value"
    Example: "25.30,512"
*/

const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const int POT_PIN = A0;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop() {
  // --- Read ultrasonic distance ---
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // timeout 30ms
  float distance_cm = duration * 0.034 / 2.0;

  // --- Read potentiometer ---
  int pot_value = analogRead(POT_PIN);

  // --- Send over serial ---
  Serial.print(distance_cm);
  Serial.print(",");
  Serial.println(pot_value);

  delay(50); // 20 Hz
}
