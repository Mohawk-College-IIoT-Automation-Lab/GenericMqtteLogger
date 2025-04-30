from paho.mqtt.client import Client, MQTTMessage
from .davids_logger import initialize_logging
import logging

class GenericMQTT:

    def __init__(self, host_name:str="localhost", host_port:int = 1883):
        
        initialize_logging("Generic Mqtt", host_name, host_port)

        self._connected = False
        self._host_name = host_name
        self._host_port = host_port
        self.mqtt_client = Client()

        self.mqtt_client.on_message = self._mqtt_default_callback
        self.mqtt_client.on_connect = self._mqtt_connect_disconnect
        self.mqtt_client.on_disconnect = self._mqtt_connect_disconnect
        self.mqtt_client.on_connect_fail = self._mqtt_failed

    def _mqtt_connect_disconnect(self, client:Client, userdata, flags, reason_code):
        # Get connection status
        self._connected = self.mqtt_client.is_connected()
        
        # Loop start/stop
        if self._connected:
            self.mqtt_client.loop_start()
        else:
            self.mqtt_client.loop_stop()

        # Loggign and emit status
        logging.info(f"[MQTT] Connection status: {self.connected}")
        
    def _mqtt_failed(self):
        self._connected = self.mqtt_client.is_connected()
        self.mqtt_client.loop_stop()
        logging.error("[MQTT] Failed to connect")

    def _mqtt_default_callback(self, client:Client, userdata, message:MQTTMessage):
        logging.info(f"[MQTT] unhandled data received from topic: {message.topic} -> {message.payload.decode()}")

    def mqtt_connect(self):
        logging.info(f"[MQTT] Attempting connection to host: {self._host_name} on port: {self._host_port}")
        
        error = self.mqtt_client.connect(self._host_name, self._host_port)
        if error:
            logging.error(f"[MQTT] Error connecting to host: {self._host_name}:{self._host_port}, error code: {error}")
            
    def mqtt_disconnect(self):
        logging.info(f"Disconnecting from {self._host_name}:{self._host_port}")
        self.mqtt_client.disconnect()

    @property
    def connected(self):
        return self._connected

    @property
    def host_name(self):
        return self._host_name

    @host_name.setter
    def host_name(self, value: str):
        if self.connected:
            logging.warning("Cannot change host name while connected")
            return
        self._host_name = value

    @property
    def host_port(self):
        return self._host_port

    @host_port.setter
    def host_port(self, value: int):
        if self.connected:
            logging.warning("Cannot change host port while connected")
            return
        self._host_port = value

if __name__ == "__main__":
    genmqtt = GenericMQTT()
