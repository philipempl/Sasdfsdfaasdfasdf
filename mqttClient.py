from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import paho.mqtt.client as mqtt
import random
import json 
import time
import threading
import uuid

host = "192.168.21.105"
port = 1883
main_topic = 'mind2/'
threads=[]
UID = uuid.uuid1()
counter = 0

def getNextInt():
    counter=+1
    return counter

class MQTTClient:

    def __init__(self,name):
        self.name = name
        self.client = mqtt.Client(name,protocol=mqtt.MQTTv5)
        self.client.on_connect = self.on_connect
        #self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe

        t = threading.Thread(target=self.looping)
        t.start()

    def publish(self,topic,payload,correlationData=None):
        topic = main_topic + topic
        properties = Properties(PacketTypes.PUBLISH)
        
        properties.CorrelationData=bytes(str(uuid.uuid1()), "utf-8") if not correlationData else correlationData

        print(properties.CorrelationData)
        counter=+1
        self.client.publish(topic, qos=2, payload=payload, properties=properties)

    def subscribe(self,topic):
        topic = main_topic + topic
        self.client.subscribe(topic, qos=2, options=None, properties=None)

    def on_publish(self, client, obj, mid):
        print(self.name + " published  (mid=" + str(mid) + ")")

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(self.name + " successfully connected to " + host + ":" + str(port))
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_subscribe(self, client, userdata, mid, granted_qos, properties):
        print(self.name + " subscribed topic with " + str(granted_qos[0]) + " S(mid=" +  str(mid) + ")")

    def on_message(self, client, userdata, message):
        print(self.name + " received message: " ,str(message.payload.decode("utf-8")))

class TemperatureSensor(MQTTClient):

    message = '{ "temperature": 0, "humidity": 0, "battery": 0, "linkquality": 0 }'

    def __init__(self,name):
        MQTTClient.__init__(self,name)
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            message_tmp = json.loads(self.message)
            message_tmp["temperature"] = random.uniform(18,26)
            message_tmp["humidity"] = random.uniform(40,90)
            message_tmp["battery"] = random.uniform(89,92)
            message_tmp["linkquality"] = random.uniform(50,255)
            self.publish(self.name, payload=json.dumps(message_tmp))
            #self.client.loop()
            time.sleep(random.randint(10,15))


class MotionSensor(MQTTClient):
    
    message = '{ "on": true, "alert": true, "battery": 0, "linkquality": 0}'

    def __init__(self,name):
        self.message = '{ "on": true, "alert": true, "battery": 0, "linkquality": 0}'
        MQTTClient.__init__(self,name)
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            decision = [True,False,False,False,False,False,False,False]
            message_tmp = json.loads(self.message)
            if(message_tmp["on"]):
                message_tmp["alert"] = decision[random.randint(0,7)]
                self.publish(self.name, payload=json.dumps(message_tmp))
                #self.publish(self.name + "/toggleState", payload=self.message)
                time.sleep(random.randint(30,60))


class WindowSensor(MQTTClient):

    message = '{ "open": true, "battery": 0, "linkquality": 0}'
    toggle = '{"open": false}'
    topic = ''
    def __init__(self,name):
        MQTTClient.__init__(self,name)            
        self.topic = self.name + "/toggleState"
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            decision = [True,False,False,False,False,False,False,False]
            message_tmp = json.loads(self.message)
            message_tmp["open"] = decision[random.randint(0,7)]
            self.publish(self.name, payload=json.dumps(message_tmp))
            #self.publish(self.name + "/toggleState", payload=self.message)
            time.sleep(random.randint(100,200))

class DoorSensor(MQTTClient):

    message = '{ "open": true, "battery": 0, "linkquality": 0}'
    toggle = '{"open": false}'
    topic = ''
    def __init__(self,name):
        MQTTClient.__init__(self,name)            
        self.topic = self.name + "/toggleState"
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            decision = [True,False,False,False,False,False,False,False]
            message_tmp = json.loads(self.message)
            message_tmp["open"] = decision[random.randint(0,7)]
            self.publish(self.name, payload=json.dumps(message_tmp))
            #self.publish(self.name + "/toggleState", payload=self.message)
            time.sleep(random.randint(100,200))


class DoorActuator(MQTTClient):

    message = '{ "open": true, "battery": 0, "linkquality": 0}'
    toggle = '{"open": false}'
    topic = ''
    def __init__(self,name):
        MQTTClient.__init__(self,name)            
        self.topic = self.name + "/toggleState"
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            time.sleep(0)

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(self.name + " successfully connected to " + host + ":" + str(port))
            self.subscribe(self.topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, message):
        message_tmp = json.loads(self.message)
        message_tmp2 = json.loads(message.payload.decode("utf-8"))
        message_tmp["open"] = message_tmp2["open"]
        self.message = json.dumps(message_tmp)
        self.publish(self.name, self.message, message.properties.CorrelationData)
        print(self.name + " received message: " ,str(message.payload.decode("utf-8")))


class FireAlarm(MQTTClient):

    message = '{ "alert": true, "battery": 0, "linkquality": 0}'
    toggle = '{"alert": false}'
    topic = ''
    def __init__(self,name):
        MQTTClient.__init__(self,name)            
        self.topic = self.name + "/toggleState"
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            time.sleep(0)

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(self.name + " successfully connected to " + host + ":" + str(port))
            self.subscribe(self.topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, message):
        time.sleep(random.randint(1,10)/1000)
        message_tmp = json.loads(self.message)
        message_tmp2 = json.loads(message.payload.decode("utf-8"))
        message_tmp["alert"] = message_tmp2["alert"]
        self.message = json.dumps(message_tmp)
        self.publish(self.name, self.message, message.properties.CorrelationData)
        print(self.name + " received message: " ,str(message.payload.decode("utf-8")))

class Thermostat(MQTTClient):

    message = '{ "active": true, "state": 0, "battery": 0, "linkquality": 0}'
    toggle = '{"active": false}'
    topic = ''
    def __init__(self,name):
        MQTTClient.__init__(self,name)            
        self.topic = self.name + "/toggleState"
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            time.sleep(0)

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(self.name + " successfully connected to " + host + ":" + str(port))
            self.subscribe(self.topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, message):
        message_tmp = json.loads(self.message)
        message_tmp2 = json.loads(message.payload.decode("utf-8"))
        message_tmp["active"] = message_tmp2["active"]
        if(message_tmp2["active"]):
            message_tmp["state"] = message_tmp2["state"]
        self.message = json.dumps(message_tmp)
        self.publish(self.name, self.message, message.properties.CorrelationData)
        print(self.name + " received message: " ,str(message.payload.decode("utf-8")))

class Shutter(MQTTClient):

    message = '{ "active": true, "percentage": 0, "battery": 0, "linkquality": 0}'
    toggle = '{"active": false}'
    topic = ''
    def __init__(self,name):
        MQTTClient.__init__(self,name)            
        self.topic = self.name + "/toggleState"
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            time.sleep(0)

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(self.name + " successfully connected to " + host + ":" + str(port))
            self.subscribe(self.topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, message):
        time.sleep(random.randint(1,10)/1000)
        message_tmp = json.loads(self.message)
        message_tmp2 = json.loads(message.payload.decode("utf-8"))
        message_tmp["active"] = message_tmp2["active"]
        if(message_tmp2["active"]):
            message_tmp["percentage"] = message_tmp2["percentage"]
        self.message = json.dumps(message_tmp)
        self.publish(self.name, self.message, message.properties.CorrelationData)
        print(self.name + " received message: " ,str(message.payload.decode("utf-8")))

class LEDBulb(MQTTClient):

    message = '{ "on": true, "battery": 0, "linkquality": 0}'
    toggle = '{"on": false}'
    topic = ''
    def __init__(self,name):
        MQTTClient.__init__(self,name)            
        self.topic = self.name + "/toggleState"
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            time.sleep(0)

    def on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print(self.name + " successfully connected to " + host + ":" + str(port))
            self.subscribe(self.topic)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, message):
        message_tmp = json.loads(self.message)
        message_tmp2 = json.loads(message.payload.decode("utf-8"))
        message_tmp["on"] = message_tmp2["on"]
        self.message = json.dumps(message_tmp)
        self.publish(self.name, self.message, message.properties.CorrelationData)
        print(self.name + " received message: " ,str(message.payload.decode("utf-8")))


class SmokeDetector(MQTTClient):
    
    message = '{ "on": true, "alert": true, "battery": 0, "linkquality": 0}'

    def __init__(self,name):
        MQTTClient.__init__(self,name)
        self.client.connect(host, port, keepalive=60)
        self.client.loop_start()

    def looping(self):
        while True:
            decision = [True,True,True,True,True,False,False,False]
            message_tmp = json.loads(self.message)
            if(message_tmp["on"]):
                message_tmp["alert"] = decision[random.randint(0,7)]
                if(message_tmp["alert"]):
                    self.publish(self.name, payload=json.dumps(message_tmp))
                #self.publish(self.name + "/toggleState", payload=self.message)
                time.sleep(random.randint(10,20))