// 0 + 1: RX & TX

uint8_t[] data_pins = {2, 3, 4, 5, 6, 7, 8, 9};
uint8_t latch_pin = 10;
uint8_t write_pin = 11;
uint8_t addr_A8_pin = 12;
uint8_t addr_A9_pin = 13;

void pulsePin(uint8_t pin) {
  digitalWrite(pin, HIGH);
  delayMicroseconds(1);
  digitalWrite(pin, LOW);
}

void setupData(uint8_t data) {
  for (uint8_t i = 0; i < 8; i++) {
    digitalWrite(data_pins[i], data & 1);
    data >>= 1;
  }
}

void setupAddress(uint16_t addr) {
  setupData(data & 0xFF);
  pulsePin(latch_pin);
  digitalWrite(addr_A8_pin, (data_pins >> 8) & 1);
  digitalWrite(addr_A9_pin, (data_pins >> 9) & 1);
}

void write(uint16_t addr, uint8_t data) {
  setupAddress(addr);
  setupData(data);
  pulsePin(write_pin);
}

void configurePins() {
  pinMode(latch_pin, OUTPUT);
  pinMode(write_pin, OUTPUT);
  pinMode(addr_A8_pin, OUTPUT);
  pinMode(addr_A9_pin, OUTPUT);

  for (uint8_t d : data_pins) {
    pinMode(d, OUTPUT);
  }
}

void setup() {
  configurePins();
  Serial.begin(9600);

  write(0, 5);
}

void loop() {
  Serial.write("\nEnter an address: ");
  addr = static_cast<uint16_t>(Serial.readStringUntil(" ").toInt());
  Serial.write("\nEnter the data to write at the address: ");
  data = static_cast<uint8_t>(Serial.readStringUntil(" ").toInt());
  Serial.write("\nWriting... ");
  write(addr, data);
  Serial.write("done!");
}
