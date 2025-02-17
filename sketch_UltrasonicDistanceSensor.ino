// Set pin out: PWR on board --> Vin, GND on board --> GND
int GREEN_LT = 16;
int RED_LT = 5;
int ECHO = 12;          // Echo pin
int TRIG = 14;          // Trigger pin

#define SOUND_VELOCITY 0.034    // 340 meter per second

long duration;          // Time from Trigger to Echo
float dist_cm;

void setup() {
  Serial.begin(115200);     // for Serial Monitor output (115200 baud)

  pinMode(TRIG, OUTPUT);    // Trigger pin --> sound output
  pinMode(ECHO, INPUT);     // Echo pin --> receiver sensor

  pinMode(GREEN_LT, OUTPUT);  // Green LED pin
  pinMode(RED_LT, OUTPUT);    // Red LED pin
}

void loop() {

  // Clear Trigger pin
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  // Send out sound signal
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  // Receive returning sound signal
  duration = pulseIn(ECHO, HIGH);
  dist_cm = duration * SOUND_VELOCITY / 2;

  // Transfer data through Serial port
  Serial.print("Distance (cm): ");
  Serial.println(dist_cm);

   //*** FIX-ME ***//

  // Wait 100 mili-seconds
  delay(100);
}
