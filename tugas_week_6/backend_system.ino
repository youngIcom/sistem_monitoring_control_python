#include <Servo.h>

// Motor A (L298N)
#define ENA D1  // PWM untuk kecepatan Motor A
#define IN1 D2  // Arah Motor A
#define IN2 D3  // Arah Motor A

// Motor B (L298N)
#define ENB D5  // PWM untuk kecepatan Motor B
#define IN3 D6  // Arah Motor B
#define IN4 D7  // Arah Motor B

// Servo
#define SERVO_PIN D4

Servo myServo;

void setup() {
  Serial.begin(9600);

  // Motor A
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  // Motor B
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Servo
  myServo.attach(SERVO_PIN);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    Serial.println("Diterima : " + input);

    if (input.startsWith("MA:")) {
      int pwm = input.substring(3).toInt();
      controlMotor(ENA, IN1, IN2, pwm);
    }
    else if (input.startsWith("MB:")) {
      int pwm = input.substring(3).toInt();
      controlMotor(ENB, IN3, IN4, pwm);
    }
    else if (input.startsWith("S:")) {
      int angle = input.substring(2).toInt();
      angle = constrain(angle, 0, 180);
      myServo.write(angle);
    }
  }
}

void controlMotor(int enPin, int in1, int in2, int pwm) {
  pwm = constrain(pwm, -255, 255);
  if (pwm > 0) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enPin, pwm);
  } else if (pwm < 0) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enPin, -pwm);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    analogWrite(enPin, 0);
  }
}
