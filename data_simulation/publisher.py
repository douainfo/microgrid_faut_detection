import time, random, json
import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

def simulate():
    # 20% faults
    is_fault = random.random() < 0.2
    if not is_fault:
        voltage = random.uniform(220,240)
        current = random.uniform(5,40)
        freq = random.uniform(49.8,50.2)
        soc = random.uniform(30,90)
        power = voltage*current/1000
        label=0; fault_type=None
    else:
        fault_type=random.choice(["undervoltage","overvoltage","overcurrent","freq"])
        if fault_type=="undervoltage":
            voltage=random.uniform(150,190); current=random.uniform(5,40)
        elif fault_type=="overvoltage":
            voltage=random.uniform(250,280); current=random.uniform(5,40)
        elif fault_type=="overcurrent":
            voltage=random.uniform(220,240); current=random.uniform(50,100)
        else:
            voltage=random.uniform(220,240); current=random.uniform(5,40)
        freq = random.uniform(47,48.5) if fault_type=="freq" else random.uniform(49,51.5)
        soc = random.uniform(10,100)
        power = voltage*current/1000
        label=1
    return {
        "voltage": voltage, "current": current, "power": power,
        "frequency": freq, "soc_battery": soc,
        "label": label, "fault_type": fault_type,
        "timestamp": time.time()
    }

if __name__=="__main__":
    while True:
        data=simulate()
        client.publish(MQTT_TOPIC, json.dumps(data))
        print("Sent",data)
        time.sleep(2)
