import paho.mqtt.client as mqtt
import json

class mqtt_helper():
    def __init__(self, location):

        # host
        self.host = "192.168.0.10"

        # topics & location
        self.location = location
        self.value_topic = "home/inside/sensor/"+str(location)
        self.status_topic = "status/sensor/"+str(location)

        # client
        self.client_label = str(location)+"_conditions"
        self.client = mqtt.Client(self.client_label)

        # last will
        offline_msg = json.dumps({"location":self.location, "status":"offline"})
        self.client.will_set(self.status_topic, payload=offline_msg, qos=0, retain=True)

        # connect
        self.client.connect(self.host, keepalive=60)

    def publish_message(self, temp, hum, batt):
        dict_msg = {"location":self.location, "temperature":temp, "humidity":hum, "battery":batt}
        msg = json.dumps(dict_msg)
        self.client.publish(self.value_topic,msg)

    def publish_status(self):
        online_msg = json.dumps({"location":self.location, "status":"online"})
        self.client.publish(self.status_topic, payload=online_msg, qos=0, retain=True)
