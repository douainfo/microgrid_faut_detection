import json
from datetime import datetime
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from config import *

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
col = db[MONGO_COLLECTION_NAME]

def on_connect(client,userdata,flags,rc):
    client.subscribe(MQTT_TOPIC)

def on_message(client,userdata,msg):
    data=json.loads(msg.payload.decode())
    data["datetime"]=datetime.fromtimestamp(data["timestamp"])
    col.insert_one(data)
    print("Saved",data)

client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message
client.connect(MQTT_BROKER,MQTT_PORT,60)
client.loop_forever()
