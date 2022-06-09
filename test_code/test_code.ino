
const int NUM_CHANNELS = 8;
const int GND_PINS[NUM_CHANNELS] = {5, 6, 7, 8, 9, 10, 11, 12};
const int MUX_PINS[3] = {2, 3, 4};
int noise[NUM_CHANNELS][NUM_CHANNELS];
int currData[NUM_CHANNELS][NUM_CHANNELS];

void setup() {
  // need to set pins to output to control mux
  for(int i = 0; i < 3; i++){
    pinMode(MUX_PINS[i], OUTPUT);
    digitalWrite(MUX_PINS[i], LOW);
  }

  // initialize all the controlled pins to the high impedance state
  for(int i = 0; i < NUM_CHANNELS; i++){
    pinMode(GND_PINS[i], INPUT);
    digitalWrite(GND_PINS[i], LOW);
  }

  for(int row = 0; row < NUM_CHANNELS; row++){
    for(int col = 0; col < NUM_CHANNELS; col++){
      noise[row][col] = 0;
    }
  }

  Serial.begin(9600);
  calibrateDiodes();
  

}

void readData(bool calibration = false){
  //if (!calibration) Serial.println("Reading...");
  for(int row = 0; row < NUM_CHANNELS; row++){
    // bridge the appropriate row to ground
    pinMode(GND_PINS[row], OUTPUT);
    digitalWrite(GND_PINS[row], LOW);

    // make counter to hold data
    int index = 0;
    //if (!calibration) Serial.print('[');
    for(int C = 0; C < 2; C++){
      digitalWrite(MUX_PINS[2], C);
      for(int B = 0; B < 2; B++){
        digitalWrite(MUX_PINS[1], B);
        for(int A = 0; A < 2; A++){
          digitalWrite(MUX_PINS[0], A);
          delay(5);
          if(!calibration){
            currData[row][index] = analogRead(A0) - noise[row][index];
          }
          else{
            currData[row][index] = analogRead(A0);
          }
          /*if(!calibration){
            Serial.print(currData[row][index]);
            Serial.print(", ");
          }*/
          index++;
        }
      }
    }
    pinMode(GND_PINS[row], INPUT);
    digitalWrite(GND_PINS[row], LOW);
    //if(!calibration) Serial.println("]");
  }
  //if(!calibration) Serial.println('\n');
}

void calibrateDiodes(){
  int numReads = 5;
  for(int row = 0; row < NUM_CHANNELS; row++){
      for(int col = 0; col < NUM_CHANNELS; col++){
        noise[row][col] = 0;
      }
    }
  for(int i = 0; i < numReads; i++){
    readData(true);
    for(int row = 0; row < NUM_CHANNELS; row++){
      for(int col = 0; col < NUM_CHANNELS; col++){
        noise[row][col] += currData[row][col];
      }
    }
  }

  for(int row = 0; row < NUM_CHANNELS; row++){
    for(int col = 0; col < NUM_CHANNELS; col++){
      noise[row][col] = (int) (((float)noise[row][col]) / numReads);
    }
  }
}

void printData(){
  char start = '-';
  for(int row = 0; row < NUM_CHANNELS; row++){
    Serial.println(start);
    Serial.println(row);
    for(int col = 0; col < NUM_CHANNELS; col++){
      Serial.print(currData[row][col]);
      Serial.print(" ");
    }
    Serial.print('\n');
  }
}

void loop() {
  readData();
  printData();

}
