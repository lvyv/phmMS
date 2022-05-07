import threading

import paho.mqtt.client as mqtt_client
from phmconfig.config import ConfigSet


class MqttClient:

    init = False
    _instance_lock = threading.Lock()

    def __init__(self):
        if MqttClient.init is False:
            MqttClient.init = True
            self.cfg = ConfigSet.get_cfg()
            self.using = self.cfg['mqtt_use_auth']
            self.clientId = self.cfg['mqtt_cid']
            self.username = self.cfg['mqtt_usr']
            self.password = self.cfg['mqtt_pwd']
            self.host = self.cfg['mqtt_svr']
            self.port = self.cfg['mqtt_port']
            self.topic = self.cfg['mqtt_tp']
            self.mqttClient = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with MqttClient._instance_lock:
                if not hasattr(cls, '_instance'):
                    MqttClient._instance = super().__new__(cls)
        return MqttClient._instance

    def start(self):
        if self.using is True:
            self.mqttClient = mqtt_client.Client(self.clientId)
            self.mqttClient.username_pw_set(self.username, self.password)
        else:
            self.mqttClient = mqtt_client.Client()
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_disconnect = self.on_disconnect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.on_subscribe = self.on_subscribe
        self.mqttClient.on_unsubscribe = self.on_unsubscribe
        self.mqttClient.on_publish = self.on_publish
        self.mqttClient.on_log = self.on_log
        self.mqttClient.connect(self.host, self.port)
        self.mqttClient.loop_start()
        # mqttClient.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        pass

    def on_disconnect(self, client, userdata, rc):
        print("disconnected with result code " + str(rc))
        pass

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        pass

    def on_unsubscribe(self, client, userdata, mid):
        pass

    def on_publish(self, client, userdata, mid):
        pass

    def on_log(self, client, userdata, level, buf):
        pass

    def publish(self, payload):
        self.mqttClient.publish(self.topic, payload)
