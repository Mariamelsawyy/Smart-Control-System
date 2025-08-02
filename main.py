import paho.mqtt.client as mqtt
import time

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPIC_TEMP = "esp32/temp"
TOPIC_RELAY = "esp32/relay/control"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC_TEMP)
    

def on_message(client, userdata, msg):
    if msg.topic == TOPIC_TEMP:
        print(f"[ESP32] Temperature: {msg.payload.decode()} °C")


   

client = mqtt.Client("")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        cmd = input("Enter command (on/off/q): ").strip().lower()
        if cmd in ["on", "off"]:
            client.publish(TOPIC_RELAY, cmd)
        elif cmd == "q":
            break
        else:
            print("Invalid command. Use 'on', 'off', or 'q' to quit.")
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
print("Disconnected.")