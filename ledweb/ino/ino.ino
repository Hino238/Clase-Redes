void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT); // Pin para Humedad
  pinMode(12, OUTPUT); // Pin para Temperatura
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    
    // Logica para Humedad
    if (cmd == "HUMEDAD_ALERTA") digitalWrite(13, HIGH);
    else if (cmd == "HUMEDAD_OK") digitalWrite(13, LOW);

    // Logica para Temperatura
    if (cmd == "TEMP_ALERTA") digitalWrite(12, HIGH);
    else if (cmd == "TEMP_NORMAL") digitalWrite(12, LOW);

    Serial.println("OK:" + cmd);
  }
}
