from paho.mqtt.client import Client, MQTTMessage, MQTTv5
from .davids_logger import initialize_logging
import logging

class GenericMQTT:

    def __init__(self, client_name:str="GenericMqtt", log_name:str="Generic MQTT", host_name:str="localhost", host_port:int = 1883):
        
        initialize_logging(process_name=log_name, broker=host_name, port=host_port)

        self._host_name = host_name
        self._host_port = host_port
        self.mqtt_client = Client(protocol=MQTTv5, client_id=client_name)

        self.mqtt_client.on_message = self._mqtt_default_callback
        self.mqtt_client.on_connect = self._mqtt_connect
        self.mqtt_client.on_disconnect = self._mqtt_connect
        self.mqtt_client.on_connect_fail = self._mqtt_failed

    def _mqtt_connect(self, client:Client, userdata, reason_code):
        logging.info(f"[MQTT][{self.mqtt_client._client_id}] Connected")

    def _mqtt_disconnect(self, client:Client, userdata, reason_code):
        logging.info(f"[MQTT][{self.mqtt_client._client_id}] Disconnected")
        if reason_code != 0:
            logging.info(f"[MQTT][{self.mqtt_client._client_id}] Trying reconnect")
            try:
                self.mqtt_client.reconnect()
            except Exception as e:
                logging.error(f"[MQTT][{self.mqtt_client._client_id}] Failed to reconnect")
        
    def _mqtt_failed(self):
        self.mqtt_client.loop_stop()
        logging.error("[MQTT][{self.mqtt_client._client_id}] Failed to connect")

    def _mqtt_default_callback(self, client:Client, userdata, message:MQTTMessage):
        logging.info(f"[MQTT][{self.mqtt_client._client_id}] unhandled data received from topic: {message.topic} -> {message.payload.decode()}")

    def mqtt_connect(self):
        logging.info(f"[MQTT][{self.mqtt_client._client_id}] Attempting connection to host: {self._host_name} on port: {self._host_port}")
        
        error = self.mqtt_client.connect(self._host_name, self._host_port, clean_start=True)
        if error:
            logging.error(f"[MQTT][{self.mqtt_client._client_id}] Error connecting to host: {self._host_name}:{self._host_port}, error code: {error}")
        self.mqtt_client.loop_forever()
            
    def mqtt_disconnect(self):
        logging.info(f"[MQTT][{self.mqtt_client._client_id}] Disconnecting from {self._host_name}:{self._host_port}")
        self.mqtt_client.disconnect()

    def publish(self, topic:str, message):
        self.mqtt_client.publish(topic=topic, payload=message)

    @property
    def connected(self):
        return self.mqtt_client.is_connected()

if __name__ == "__main__":
    genmqtt = GenericMQTT()
