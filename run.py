"""
Module for simulating a dynamic number of different MQTT clients, i.e. sensors and actuators.
Each client is run in its own thread.
"""

# pylint: disable=too-many-arguments, unused-argument

from abc import abstractmethod
from datetime import datetime
import json
import logging
import random
import threading
import time
import uuid
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import paho.mqtt.client as mqtt
import time

logger = logging.getLogger('Evaluation')
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel("DEBUG")
ch.setLevel("DEBUG")


def get_next_random(lower: int, upper: int) -> float:
    """
    Function for getting a new random number with 'lower' and 'upper'
    with two-digit precision.
    """
    return round(random.uniform(lower, upper), 2)


class MQTTClient():
    """
    Abstract class for MQTT-based clients.
    Handles basic callbacks, logging, and instantiation of paho.mqtt.client
    """
    broker_url = "192.168.2.171"
    broker_port = 1883
    main_topic = "evaluation"

    @abstractmethod
    def __init__(self, topic: str, interval: int, enable_detailed_logger=False):
        self.name = topic
        self.interval = interval
        self.client = mqtt.Client(client_id=self.name, protocol=mqtt.MQTTv5)
        self.topic = f"{self.main_topic}/{topic}"
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.on_publish = self.__on_publish
        self.client.on_subscribe = self.__on_subscribe
        self.client.on_unsubscribe = self.__on_unsubscribe
        self.client.on_message = self.__on_message

        if enable_detailed_logger:
            self.client.enable_logger(logger)

    def connect(self):
        """
        Helper function to connect to the MQTT-broker using paho.mqtt.client
        """
        self.client.connect(self.broker_url, self.broker_port, keepalive=60)

    def publish(self, payload: str, correlation_data: str = None):
        """
        Helper function to publish a message to a topic of the MQTT-broker using paho.mqtt.client
        """
        properties = Properties(PacketTypes.PUBLISH)
        properties.CorrelationData = str(datetime.now()).encode('utf-8')
        self.client.publish(self.topic, qos=0, payload=payload, properties=properties, retain=False)

    def subscribe(self, topic):
        """
        Helper function to subscribe to a topic of the MQTT-broker using paho.mqtt.client
        """
        self.client.subscribe(topic, qos=2, options=None, properties=None)

    def __on_publish(self, client, userdata, mid):
        #logger.info("%s published (Mid: %s)", self.name, mid)
        pass

    def __on_connect(self, client, userdata, flags, response_code, properties):
        if response_code == 0:
            logger.info("\033[0;36m %s connected to %s:%s \033[0m", self.name, self.broker_url, self.broker_port)
        else:
            logger.warning("Failed to connect, return code %d\n", response_code)

    def __on_disconnect(self, client, userdata, flags, response_code):
        logger.info("\033[0;36m %s disconnected from %s:%s \033[0m", self.name, self.broker_url, self.broker_port)
        

    def __on_subscribe(self, client, userdata, mid, granted_qos, properties):
        #logger.info("%s subscribed '%s' with QoS %s (mid=%s)", self.name, self.topic, granted_qos[0], mid)
        pass

    def __on_unsubscribe(self, client, userdata, mid, granted_qos, properties):
        #logger.info("%s unsubscribed from '%s'", self.name, self.topic)
        pass

    def __on_message(self, client, userdata, message):
        #logger.info("%s received message: %s", self.name, message.payload.decode('utf-8'))
        pass


class MQTTSensor(MQTTClient):
    """
    Abstract class for a simple MQTT-based sensor based on the abstract MQTTClient class.
    The sensor publishes simulated status updates to a topic named after the sensor itself.
    """
    @abstractmethod
    def __init__(self, client_name: str, interval: int, simulation):
        super().__init__(client_name, interval)
        self.connect()
        self.client.loop_start()
        self.__tick = simulation
        self.interval = interval

    def loop(self):
        """
        Function to keep the sensor alive within its independent thread.
        """
        while SIMULATION_ALIVE and SIMULATION_ALIVE2:
            self.__tick()
        self.client.disconnect()

class MQTTDivider(MQTTClient):
    """
    Abstract class for a simple MQTT-based sensor based on the abstract MQTTClient class.
    The sensor publishes simulated status updates to a topic named after the sensor itself.
    """
    @abstractmethod
    def __init__(self, client_name: str, interval: int, simulation):
        super().__init__(client_name, interval)
        self.connect()
        self.__tick = simulation
        self.interval = interval

    def loop(self):
        """
        Function to keep the sensor alive within its independent thread.
        """
        self.__tick()
        self.client.disconnect()

class TemperatureSensor(MQTTSensor):
    """
    Object simulating an MQTT-based temperature sensor.
    """
    def __init__(self, sensor_name: str, interval: int):
        super().__init__(sensor_name, interval, self.__simulation)

    def __simulation(self):
        message = {
            "temperature": get_next_random(10, 30),
            "humidity": get_next_random(40, 90),
            "battery": get_next_random(89, 92),
            "linkquality": get_next_random(50, 255)}
        self.publish(payload=json.dumps(message))
        time.sleep(1/self.interval)

class Divider(MQTTDivider):
    """
    Object simulating an MQTT-based temperature sensor.
    """
    def __init__(self, sensor_name: str, interval: int):
        super().__init__(sensor_name, interval, self.__simulation)

    def __simulation(self):
        message = {
            "temperature": get_next_random(10, 30),
            "humidity": get_next_random(40, 90),
            "battery": get_next_random(89, 92),
            "linkquality": get_next_random(50, 255)}
        self.publish(payload=json.dumps(message))



if __name__ == "__main__":
    SIMULATION_ALIVE2 = True
    SIMULATION_ALIVE = True
    logger.info(" =======================================================")
    logger.info("                                                        ")
    logger.info("                                                        ")
    logger.info("         ____    _____      _      ____    _____        ")
    logger.info("        / ___|  |_   _|    / \    |  _ \  |_   _|       ")
    logger.info("        \___ \    | |     / _ \   | |_) |   | |         ")
    logger.info("         ___) |   | |    / ___ \  |  _ <    | |         ")
    logger.info("        |____/    |_|   /_/   \_\ |_| \_\   |_|         ")
    logger.info("                                                        ")
    logger.info("                                                        ")

    pointer = 40
    msg_max = 10000
    interval = 1
    steps = 10
    while pointer < msg_max:
        logger.info(f"Evaluation run using 10 clients producing {pointer} messages.")
        SIMULATION_ALIVE = True
        # include one client to seperate
        thread000= threading.Thread(name="DIVIDER", target=Divider("DIVIDER",interval).loop).start()
        time.sleep(10)

        measure = time.time() + 60
        thread1 = threading.Thread(name="temperature-sensor1", target=TemperatureSensor("temperature-sensor1",interval).loop).start()
        thread2 = threading.Thread(name="temperature-sensor2", target=TemperatureSensor("temperature-sensor2",interval).loop).start()
        thread3 = threading.Thread(name="temperature-sensor3", target=TemperatureSensor("temperature-sensor3",interval).loop).start()
        thread4 = threading.Thread(name="temperature-sensor4", target=TemperatureSensor("temperature-sensor4",interval).loop).start()
        thread5 = threading.Thread(name="temperature-sensor5", target=TemperatureSensor("temperature-sensor5",interval).loop).start()
        thread6 = threading.Thread(name="temperature-sensor6", target=TemperatureSensor("temperature-sensor6",interval).loop).start()
        thread7 = threading.Thread(name="temperature-sensor7", target=TemperatureSensor("temperature-sensor7",interval).loop).start()
        thread8 = threading.Thread(name="temperature-sensor8", target=TemperatureSensor("temperature-sensor8",interval).loop).start()
        thread9 = threading.Thread(name="temperature-sensor9", target=TemperatureSensor("temperature-sensor9",interval).loop).start()
        thread10 = threading.Thread(name="temperature-sensor10", target=TemperatureSensor("temperature-sensor10",interval).loop).start()

        while time.time() < measure:
            pass
        SIMULATION_ALIVE = False

        interval = interval + 1
        pointer = pointer + steps
        time.sleep(10)
        
    while SIMULATION_ALIVE2:
        try:
            time.sleep(.1)
        except KeyboardInterrupt:
            SIMULATION_ALIVE2 = False

    logger.info("Unsubscribing and disconnecting clients. This may take a while...")
    logger.info(" =======================================================")
    logger.info("                                                        ")
    logger.info("                                                        ")
    logger.info("                 _____   _   _   ____                   ")
    logger.info("                | ____| | \ | | |  _ \                  ")
    logger.info("                |  _|   |  \| | | | | |                 ")
    logger.info("                | |___  | |\  | | |_| |                 ")
    logger.info("                |_____| |_| \_| |____/                  ")
    logger.info("                                                        ")
    logger.info("                                                        ")
    logger.info("                                                        ")
