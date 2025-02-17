#define TRIG_PIN 9  // HC-SR04 Trigger Pin
#define ECHO_PIN 10 // HC-SR04 Echo Pin
#define RED_LED 3   // Red LED Pin
#define GREEN_LED 4 // Green LED Pin

void setup() {
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(RED_LED, OUTPUT);
    pinMode(GREEN_LED, OUTPUT);
    
    Serial.begin(9600); // Start serial communication
}

void loop() {
    long duration;
    float distance;

    // Send a 10-microsecond pulse to trigger the sensor
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    // Measure the time for the echo
    duration = pulseIn(ECHO_PIN, HIGH);

    // Calculate the distance in cm (speed of sound is 343m/s or 0.0343 cm/µs)
    distance = (duration * 0.0343) / 2;

    // Print distance to the Serial Monitor
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    // Control LEDs based on distance
    if (distance < 10) {
        digitalWrite(RED_LED, HIGH);
        digitalWrite(GREEN_LED, LOW);
    } else {
        digitalWrite(RED_LED, LOW);
        digitalWrite(GREEN_LED, HIGH);
    }

    delay(500); // Wait for half a second before measuring again
}