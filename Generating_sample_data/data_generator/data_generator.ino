/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  
}

static int Toffset = 0;
static int Tcoeff = 20; // 10mV in digital = (.01/5)*1024 = 20.48


// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pins:
  float tempValue = (analogRead(A4) - Toffset)/Tcoeff; // Vout = Tc*Ta +V0 --> Tambient = (Vout-V0)/Tc with Tc = 10mV/C
  int windSpeedValue = analogRead(A5);
  int windDirection = (int) (360*analogRead(A6))/1024;
  float humidityValue = analogRead(A7)/10.24;
  String outPut = "Temperature: " + String(tempValue);
  outPut += " C \nWind Speed: "+ String(windSpeedValue) +  " knots at " +String( windDirection) ;
  outPut += " degrees \nHumidity: "+ String(humidityValue) + " ";

  
  // print out the value you read
  Serial.println(outPut);
  delay(1000);        // delay in between reads for stability
}
