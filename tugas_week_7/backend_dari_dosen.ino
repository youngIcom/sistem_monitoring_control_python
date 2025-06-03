#include <Servo.h>  // Library untuk servo

#define PWMA D1  // Right side motor speed control (PWM)
#define PWMB D2  // Left side motor speed control (PWM)
#define DA D3    // Right side motor direction
#define DB D4    // Left side motor direction

//// Pin untuk Sensor Garis
...

#define SERVO_PIN D0  // Pin untuk servo 

Servo myServo;

String buff, buff_motor, buff_servo;
const char delimiter[] = ":";  // The delimiter
int motor, servo;
int sensor1, sensor2, sensor3, sensor4, sensor5;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
//  Serial2.begin(115200);
//  Serial2.println("Program Dimulai");

  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(DA, OUTPUT);
  pinMode(DB, OUTPUT);

  ...
  ...
  ...
  ...

  // Initialize motors to stop
  digitalWrite(PWMA, LOW);
  digitalWrite(PWMB, LOW);
  digitalWrite(DA, LOW);
  digitalWrite(DB, LOW);

  myServo.attach(SERVO_PIN);
  myServo.write(0);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
// ****************************** MAIN CODE RUNS HERE ********************** //
  sensor();

  if (Serial.available() > 0) {
    
    // read the oldest byte in the serial buffer:
    buff = Serial.readString();// read the incoming data as string
//    Serial1.println(buff);  //debugging purpose
    
    if (buff[0] == 'M'){
      buff_motor=buff;

      // Convert String to a mutable character array
      char buff_motor_array[buff_motor.length() + 1]; // Create a buffer
      buff_motor.toCharArray(buff_motor_array, sizeof(buff_motor_array)); // Convert String to char array

      // Use strtok() to split
    char *token = strtok(buff_motor_array, delimiter);
    if (token != NULL) {
        token = strtok(NULL, delimiter);
        if (token != NULL) {
            motor = atoi(token);  // Convert second token to integer
        }
    }
    forward(motor);
    delay(1000);
    }
    
    else if (buff[0] == 'S'){
      buff_servo=buff;
      
      // Convert String to a mutable character array
      char buff_servo_array[buff_servo.length() + 1]; // Create a buffer
      buff_servo.toCharArray(buff_servo_array, sizeof(buff_servo_array)); // Convert String to char array

      // Use strtok() to split
    char *token = strtok(buff_servo_array, delimiter);
    if (token != NULL) {
        token = strtok(NULL, delimiter);
        if (token != NULL) {
            servo = atoi(token);  // Convert second token to integer
        }
    }
    myServo.write(servo);

    }
  }
// ****************************** End of Code ********************** //

}

void sensor(){
  ...
  ...
}


void forward(int num) {
  Serial.println("Moving forward...");
  digitalWrite(DA, HIGH); // Right motor forward
  digitalWrite(DB, HIGH); // Left motor forward
  analogWrite(PWMA, num); // Adjust the value (0-255) for speed control
  analogWrite(PWMB, num); // Adjust the value (0-255) for speed control
}

void backward(int num) {
  Serial.println("Moving backward...");
  digitalWrite(DA, LOW); // Right motor backward
  digitalWrite(DB, LOW); // Left motor backward
  analogWrite(PWMA, num); // Adjust the value (0-255) for speed control
  analogWrite(PWMB, num); // Adjust the value (0-255) for speed control
}

void stopMotors() {
  Serial.println("Stopping motors...");
  digitalWrite(DA, LOW);  // Right motor stop
  digitalWrite(DB, LOW);  // Left motor stop
  digitalWrite(PWMA, LOW); // Right motor speed off
  digitalWrite(PWMB, LOW); // Left motor speed off
}