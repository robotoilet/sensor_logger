import os
import re

import paho.mqtt.client as mqtt

import sensor_config

CONFIG = sensor_config.CONFIG


def checksum(s):
    """
    Made up checksum calculation based on
        - first timestamp in the string
        - sum of the ascii values of all characters in the string

    TODO: replace with standard md5 once arduino compatibility drops
    """
    timestamp = re.findall('\d{10}', s)[0]
    bytesum = reduce(lambda m,c: m + ord(c), s, 0)
    return "%s:%s" % (timestamp, bytesum)

def label_as_sent(client, userdata, msg):
    print("re-labelling file %s to be sent.." % client.send_attempt)
    os.rename(client.send_attempt,
              re.sub('C(?=\d{10})', 'S', client.send_attempt))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("verifiedData")

def delete_sent(client, userdata, msg):
    print(msg.topic + "  " + str(msg.payload))
    if msg.topic == "verifiedData":
        filepath = 'S' + re.findall('\d{10}', msg.payload)[0]
        os.remove(os.path.join(CONFIG['logdir'], filepath))
        print("removed file %s cause transfer was successful" % filepath)

def send_data(filename):
    logdir = CONFIG['logdir']
    filepath = os.path.join(logdir, filename)
    with open(filepath, 'r') as f:
        to_send = f.read()
        print("sending to server: %s" % to_send)
        client.connect(CONFIG['server'])
        client.send_attempt = filepath
        client.publish(checksum(to_send), to_send)
        client.loop_start()

client = mqtt.Client(CONFIG['site'])
client.send_attempt = None
client.username_pw_set(*CONFIG['credentials'])
client.on_connect = on_connect
client.on_message = delete_sent
client.on_publish = label_as_sent
client.subscribe("verifiedData")
