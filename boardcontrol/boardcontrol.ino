#define LEN 8

String START = "-";
int MUXPINS[3] = {10,11,12};
int DRIVEPINS[LEN] = {2,3,4,5,6,7,8,9};
int RDPIN = A0;
int MATRIX[LEN][LEN];



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  for(int a: MUXPINS)
    pinMode(a, OUTPUT);
  for(int a: DRIVEPINS){
    pinMode(a, INPUT);
    digitalWrite(a, LOW);
  }
}


void loop() {
  for(int k=0; k<LEN; k++){
    digitalWrite(MUXPINS[0], k%2);
    digitalWrite(MUXPINS[1], (k/2)%2);
    digitalWrite(MUXPINS[2], (k/4)%2);
    String rdout = "";
    delay(5);
    for(int i=0; i<LEN; i++){
      pinMode(DRIVEPINS[i], OUTPUT);
      digitalWrite(DRIVEPINS[i], HIGH);
      delay(5);
      rdout = rdout + " " + analogRead(RDPIN);
      pinMode(DRIVEPINS[i], INPUT);
      digitalWrite(DRIVEPINS[i], LOW);
    }
    Serial.println(START);
    Serial.println(k);
    Serial.println(rdout);
  }
}

void loop2() {
  for(int k=0;k<LEN;k++){
    String rdout = ""; 
    digitalWrite(DRIVEPINS[k], 1);
    for(int i=0;i<LEN;i++){
      digitalWrite(MUXPINS[0], i%2);
      digitalWrite(MUXPINS[1], (i/2)%2);
      digitalWrite(MUXPINS[2], (i/4)%2);
      /*
      Serial.print(i%2);
      Serial.print((i/2)%2);
      Serial.print((i/4)%2);
      Serial.println();
      */
      delay(5000);
      //Serial.println("" + i%2 + (i/2)%2 + (i/4)%2);
      rdout = rdout + " " + analogRead(RDPIN);
    }
    digitalWrite(DRIVEPINS[k], 0);
    Serial.println(START);
    Serial.println(k);
    Serial.println(rdout);
  }
}
