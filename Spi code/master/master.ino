#include <SPI.h>

#define DB_CAP 50
#define SS_2 10

String gate_1_passes[DB_CAP];
String gate_2_passes[DB_CAP];
int gate_1_pos = 0;
int gate_2_pos = 0;

int currentIndex = 0; // Current index in the array

unsigned long counter = 0;

void setup(void) {
  Serial.begin(115200);

  pinMode(SS_2, OUTPUT);
  digitalWrite(SS, HIGH);  // ensure SS stays high for now
  digitalWrite(SS_2, HIGH);
  // Put SCK, MOSI, SS pins into output mode
  // also put SCK, MOSI into LOW state, and SS into HIGH state.
  // Then put SPI hardware into Master mode and turn SPI on
  SPI.begin();

  // Slow down the master a bit
  SPI.setClockDivider(SPI_CLOCK_DIV8);
}

byte transferAndWait(const byte what) {
  byte a = SPI.transfer(what);
  delayMicroseconds(20);
  return a;
}

void loop(void) {
  slave_1_poll();
  slave_2_poll();
  // register_user(1);
  if (Serial.available() > 0) {
    // Read the incoming string until a newline character is received
    String receivedString = Serial.readStringUntil('\n');


    // Check if the received string has exactly 32 characters
    if (receivedString.length() == 1) {
      // Remove the trailing newline character
      receivedString.trim();
      if (receivedString == "1") {
        // Serial.println(receivedString);
        register_user(1);
      } else if (receivedString == "2") {
        // Serial.println(receivedString);
        register_user(2);
      } else{
        // Serial.println(receivedString);
        Serial.println("Something went wrong");
      }
    }
    else{
      Serial.println("length issue");
    }
  }
}

void slave_1_poll() {
  byte user_input[9];
  bool user_verified = false;

  // enable Slave Select
  digitalWrite(SS, LOW);

  byte has_input = transferAndWait('n');  // add command
  if (has_input == 1) {
    for (int i = 0; i < 9; i++) {
      user_input[i] = transferAndWait(i);
    }
    user_input[8] = 'n';
    for (int i = 0; i < 9; i++) {
      // Serial.print(char(user_input[i]));
    }
    Serial.println("");

    String user_input_str = byteArrayToString(user_input, 9);
    // verify whether token is present in the slave_1_passes
    for (int i = 0; i < DB_CAP; i++) {
      if (user_input_str == gate_1_passes[i]) {

        // send reply to the slave_1
        user_verified = true;
        removeStringFromArray(gate_1_passes, DB_CAP, user_input_str);
      }
    }
  }
  digitalWrite(SS, HIGH);
  delay(500);
  if (user_verified) {
    send_verification_to_slave_1();
  }
  else{
    // send_not_verified_to_slave_1();
  }
}

void slave_2_poll() {
  byte user_input[9];
  bool user_verified = false;

  // enable Slave Select
  digitalWrite(SS_2, LOW);

  byte has_input = transferAndWait('n');  // add command
  if (has_input == 1) {
    for (int i = 0; i < 9; i++) {
      user_input[i] = transferAndWait(i);
    }
    user_input[8] = 'n';
    for (int i = 0; i < 9; i++) {
      // Serial.print(char(user_input[i]));
    }
    // Serial.println("");

    String user_input_str = byteArrayToString(user_input, 9);
    // verify whether token is present in the slave_2_passes
    for (int i = 0; i < DB_CAP; i++) {
      if (user_input_str == gate_2_passes[i]) {
        // Serial.print("User verified in gate_2, UUID: ");
        // Serial.println(user_input_str);
        // send reply to the slave_1
        user_verified = true;
        removeStringFromArray(gate_2_passes, DB_CAP, user_input_str);
      }
    }
  }
  // disable Slave Select
  digitalWrite(SS_2, HIGH);
  delay(500);
  if (user_verified) {
    send_verification_to_slave_2();
  } else{
    // send_not_verified_to_slave_2();
  }
}

void send_verification_to_slave_1() {
  digitalWrite(SS, LOW);
  transferAndWait('g');
  digitalWrite(SS, HIGH);
  delay(500);
}

void send_verification_to_slave_2() {
  digitalWrite(SS_2, LOW);
  transferAndWait('g');
  digitalWrite(SS_2, HIGH);
  delay(500);
}

void send_not_verified_to_slave_1() {
  digitalWrite(SS, LOW);
  transferAndWait('n');
  digitalWrite(SS, HIGH);
  delay(500);
}

void send_not_verified_to_slave_2() {
  digitalWrite(SS_2, LOW);
  transferAndWait('n');
  digitalWrite(SS_2, HIGH);
  delay(500);
}

String byteArrayToString(byte byteArray[], int length) {
  String result = "";
  for (int i = 0; i < length; i++) {
    result += char(byteArray[i]);
  }
  return result;
}

// Function to remove a specific string from the array
void removeStringFromArray(String stringArray[], int arrayLength, const String &stringToRemove) {
  // Find the index of the string to remove
  int indexToRemove = -1;
  for (int i = 0; i < arrayLength; i++) {
    if (stringArray[i] == stringToRemove) {
      indexToRemove = i;
      break;
    }
  }

  // If the string was found, remove it
  if (indexToRemove != -1) {
    for (int i = indexToRemove; i < arrayLength - 1; i++) {
      stringArray[i] = stringArray[i + 1];
    }
    // Clear the last element to avoid duplicates
    stringArray[arrayLength - 1] = "";
    // Update the array length to reflect the removal
    arrayLength--;
 }
}

String generateAlphaNumericCode() {
  // Get current timestamp
  unsigned long timestamp = millis();

  // Increment counter for uniqueness
  counter++;

  // Combine timestamp, counter, and a random factor
  unsigned long combinedValue = timestamp * 10000 + counter + random(1000);

  // Characters for mapping (0-9 and a-z)
  const char characters[] = "0123456789abcdefghijklmnopqrstuvwxyz";

  // Convert to alphanumeric string
  char alphanumericString[10];  // 9 characters + null terminator
  for (int i = 0; i < 9; i++) {
    int index = combinedValue % 36;  // Use modulo to map to characters (0-35)
    alphanumericString[i] = characters[index];
    combinedValue /= 36;
  }
  alphanumericString[9] = '\0';  // Null terminator

  return String(alphanumericString);
}



// function to receive the gate number and generate token and put it into relevant gate
void register_user(int gate_num) {
  if (gate_num == 1) {
    String temp_id = generateAlphaNumericCode();
    temp_id[8] = 'n';
    Serial.println(temp_id);
    gate_1_passes[gate_1_pos] = temp_id;
    if (gate_1_pos == (DB_CAP - 1)) {
      gate_1_pos = 0;
    } else {
      gate_1_pos++;
    }
  } else {  // if this is for gate_2
    String temp_id = generateAlphaNumericCode();
    temp_id[8] = 'n';
    Serial.println(temp_id);
    gate_2_passes[gate_2_pos] = temp_id;
    if (gate_2_pos == (DB_CAP - 1)) {
      gate_2_pos = 0;
    } else {
      gate_2_pos++;
    }
  }
}