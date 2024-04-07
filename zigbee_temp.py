import paho.mqtt.client as mqtt
import json
from mqtt_helper import mqtt_helper

location = "lounge"

mqtt_helper = mqtt_helper(location)
server_address = "192.168.0.10"

topic_temp_zigbee_lounge = "zigbee2mqtt/temp_sensor_lounge"

lounge_temp = 21

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(topic_temp_zigbee_lounge,0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global lounge_temp
    
    try: 
        data = msg.payload.decode("utf-8")
        jsonData=json.loads(data)    
        temp = jsonData["temperature"]
        hum = jsonData["humidity"]
        batt = jsonData["battery"]
        mqtt_helper.publish_message(temp, hum, batt)
        mqtt_helper.publish_status()

    except Exception as e:
        print("Couldn't parse raw data: %s" % data, e)
    

client1 = mqtt.Client()
client1.on_connect = on_connect
client1.on_message = on_message

client1.connect(server_address)

client1.loop_forever()