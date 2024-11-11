import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Set up GPIO pin for controlling the motor relay
motor_relay_pin = 17  # GPIO pin for motor relay (for soil moisture)

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_relay_pin, GPIO.OUT)

# Define soil moisture threshold
SOIL_MOISTURE_THRESHOLD = 300  # Adjust based on calibration

def on_message_soil_moisture(client, userdata, msg):
    try:
        soil_moisture = float(msg.payload.decode())
        print(f"Received soil moisture level: {soil_moisture}")

        if soil_moisture < SOIL_MOISTURE_THRESHOLD:
            GPIO.output(motor_relay_pin, GPIO.LOW)
            print("Soil moisture is low, Motor turned ON")
        else:
            GPIO.output(motor_relay_pin, GPIO.HIGH)
            print("Soil moisture is sufficient, Motor turned OFF")
        print('')
    except ValueError as e:
        print(f"Error parsing soil moisture level: {e}")

# MQTT client setup
client = mqtt.Client()
client.connect("broker.hivemq.com", 1883)

# Subscribe to the soil moisture topic
client.subscribe("SoilMoisture", qos=0)

# Assign callback for soil moisture
client.message_callback_add("SoilMoisture", on_message_soil_moisture)

# Run MQTT loop
client.loop_forever()