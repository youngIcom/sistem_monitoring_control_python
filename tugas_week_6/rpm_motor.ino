#include <Servo.h>

// Pin untuk motor DC
#define IN1 D5    // GPIO14
#define IN2 D6    // GPIO12
#define ENA D7    // GPIO13 (PWM)

// Pin untuk servo
#define SERVO_PIN 16  // D0 = GPIO16 (NB: GPIO16 tidak support PWM di Servo library)

// NOTE: Lebih baik pakai pin D4 (GPIO2) atau D1/D2 (GPIO5/GPIO4) untuk Servo di ESP8266
Servo myServo;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  myServo.attach(D4);  // Gunakan GPIO2 (D4) sebagai alternatif, karena GPIO16 tidak mendukung PWM

  Serial.begin(9600);
  Serial.println("Siap menerima perintah PWM dan Servo...");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // hilangkan spasi dan newline

    if (input.startsWith("M")) {
      int pwm = input.substring(1).toInt();
      pwm = constrain(pwm, 0, 255);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, pwm);
      Serial.print("PWM diterima: ");
      Serial.println(pwm);
    }
    else if (input.startsWith("S")) {
      int angle = input.substring(1).toInt();
      angle = constrain(angle, 0, 180);
      myServo.write(angle);
      Serial.print("Servo angle diterima: ");
      Serial.println(angle);
    }
  }
}
