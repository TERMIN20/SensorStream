import paho.mqtt.client as mqtt
import time

mqttBroker = "mqtt.eclipseprojects.io"
cl = mqtt.Client("sensor")
cl.connect(mqttBroker)

while True:
    pH = "test"
    cl.publish("SensorData", pH)
    print(pH)
    time.sleep(1)