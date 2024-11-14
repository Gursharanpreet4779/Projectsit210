#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>
#include <DHT.h>
#include <SimpleTimer.h>

SimpleTimer timer;

char ssid[] = "Redmi";                // Your WiFi network name
char pass[] = "12345678";              // Your WiFi password
char broker[] = "mqtt-dashboard.com";  // MQTT broker address
const char soilMoistureTopic[] = "SoilMoisture"; // MQTT topic for soil moisture
const char dhtTopic[] = "DHT";                    // MQTT topic for DHT sensor
const char npkTopic[] = "NPK";                    // MQTT topic for NPK sensor

WiFiClient wifiClient;                // WiFi client instance
MqttClient client(wifiClient);        // MQTT client instance

#define DHTPIN 2                      // DHT sensor pin
#define DHTTYPE DHT11                 // DHT sensor type (DHT11)
DHT dht(DHTPIN, DHTTYPE);             // DHT sensor instance

void setup() {
  Serial.begin(9600);

  // Connect to WiFi
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi.");

  dht.begin();

  // Connect to MQTT broker
  while (!client.connect(broker, 1883)) {
    Serial.print("MQTT CONNECTION FAILED: ");
    Serial.println(client.connectError());
    delay(1000);
  }
  Serial.println("Connected to MQTT broker.");
}

void loop() {
  client.poll();  // Keep MQTT connection alive
  
  // Generate random soil moisture value (range: 0-1023)
  int soilMoistureValue = random(0, 1024);
  Serial.println("Soil Moisture Value: " + String(soilMoistureValue));

  // Generate random temperature (range: 20-30°C) and humidity (range: 30-60%)
  float temperature = random(200, 301) / 10.0;
  float humidity = random(300, 601) / 10.0;
  
  // Generate random NPK sensor values (range: 0-100 for each nutrient)
  float nitrogen = random(0, 101);
  float phosphorus = random(0, 101);
  float potassium = random(0, 101);
  
  Serial.print("Nitrogen Level: ");
  Serial.println(nitrogen);
  Serial.print("Phosphorus Level: ");
  Serial.println(phosphorus);
  Serial.print("Potassium Level: ");
  Serial.println(potassium);

  // Publish soil moisture data to Raspberry Pi through MQTT
  if (client.connected()) {
    if (client.beginMessage(soilMoistureTopic)) {
      client.print(soilMoistureValue);
      client.endMessage();
      Serial.println("Published Soil Moisture Value: " + String(soilMoistureValue));
    }
  }

  // Publish temperature and humidity data if valid
  if (!isnan(temperature) && !isnan(humidity)) {
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");

    if (client.beginMessage(dhtTopic)) {
      client.print("Temperature: " + String(temperature) + "°C, Humidity: " + String(humidity) + "%");
      client.endMessage();
      Serial.println("Published Temperature and Humidity.");
    }
  } else {
    Serial.println("Failed to read from DHT sensor!");
  }

  // Publish NPK sensor data
  if (client.connected()) {
    if (client.beginMessage(npkTopic)) {
      client.print("Nitrogen: " + String(nitrogen) + " mg/L, Phosphorus: " + String(phosphorus) + " mg/L, Potassium: " + String(potassium) + " mg/L");
      client.endMessage();
      Serial.println("Published NPK values.");
    }
  }
  
  delay(2000);  // Delay to avoid spamming MQTT messages
}
