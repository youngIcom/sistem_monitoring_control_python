
#include <Servo.h>  // Library untuk servo

// Pin untuk Motor DC
#define  // Pin PWM untuk mengontrol kecepatan motor 
#define   // Pin untuk mengontrol arah motor
#define ...  // Pin untuk mengontrol arah motor

String buff, buff_motor;
const char delimiter[] = ":";  // Pemisah
int motor;

void setup() {
  Serial.begin(115200);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);

  stopMotor(0);  // Pastikan motor berhenti saat awal
}

void loop() {
  if (Serial.available() > 0) {
    buff = Serial.readString(); // Baca data dari serial

    if (buff[0] == 'M'){
      ...
    }
  }
}

void forward(int num) {
  ...
}

void reverse(int num) {
  ...
}

void stopMotor(int num) {
  ...
}
