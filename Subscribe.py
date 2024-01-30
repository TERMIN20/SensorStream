import paho.mqtt.client as mqtt
import time

mqttBroker = "mqtt.eclipseprojects.io"
cl = mqtt.Client("reader")
cl.connect(mqttBroker)

def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

cl.loop_start()
cl.subscribe("SensorData")
cl.on_message = on_message
time.sleep(30)
cl.loop_end()