// 0 + 1: RX & TX

uint8_t data_pins[] = {2, 3, 4, 5, 6, 7, 8, 9};
uint8_t latch_pin = 10;
uint8_t write_pin = 11;
uint8_t addr_A8_pin = 12;
uint8_t addr_A9_pin = 13;


void pulseLatch() {
  digitalWrite(latch_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(latch_pin, LOW);
}

void pulseWrite() {
  digitalWrite(write_pin, LOW);
  delayMicroseconds(1);
  digitalWrite(write_pin, HIGH);
}

void setupData(uint8_t data) {
  for (uint8_t i = 0; i < 8; i++) {
    digitalWrite(data_pins[i], (data >> i) & 1);
    // Serial.print(i);
    // Serial.print(" ");
    // Serial.println((data >> i) & 1);
  }
}

void setupAddress(uint16_t addr) {
  for (uint8_t i = 0; i < 8; i++) {
    digitalWrite(data_pins[7 - i], (addr >> i) & 1);
  }

  pulseLatch();
  digitalWrite(addr_A8_pin, (addr >> 8) & 1);
  digitalWrite(addr_A9_pin, (addr >> 9) & 1);
}

void write(uint16_t addr, uint8_t data) {
  setupAddress(addr);
  setupData(data);
  delayMicroseconds(100);
  pulseWrite();
  delayMicroseconds(100);
}

void configurePins() {
  pinMode(latch_pin, OUTPUT);
  pinMode(write_pin, OUTPUT);
  pinMode(addr_A8_pin, OUTPUT);
  pinMode(addr_A9_pin, OUTPUT);

  digitalWrite(write_pin, HIGH);

  for (uint8_t d : data_pins) {
    pinMode(d, OUTPUT);
  }
}

void setup() {
  configurePins();
  Serial.begin(115200);

  write(0, 5);
}

void loop() {
  Serial.println("Enter address and data:");

  while (!Serial.available()) {}

  String input = Serial.readStringUntil('\n');

  int addr = 0;
  int data = 0;

  int parsed = sscanf(input.c_str(), "%d %d", &addr, &data);

  if (parsed == 2) {
    Serial.print("Address: ");
    Serial.println(addr);

    Serial.print("Data: ");
    Serial.println(data);

    Serial.print("Writing... ");
    write((uint16_t)addr, (uint8_t)data);
    Serial.println("done!");
  } else {
    Serial.println("Invalid input. Please enter two numbers separated by space.");
  }
}
