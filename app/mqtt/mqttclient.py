import paho.mqtt.client as mqtt_client
from phmconfig.config import ConfigSet
from mqtt.payload_process  import  PayloadProcess


class MqttClient:

    def __init__(self):
        self.cfg = ConfigSet.get_cfg()
        self.using = self.cfg['ms_mqtt_using']
        self.clientId = self.cfg['ms_mqtt_cid']
        self.username = self.cfg['ms_mqtt_usr']
        self.password = self.cfg['ms_mqtt_pwd']
        self.host = self.cfg['ms_mqtt_svr']
        self.port = self.cfg['ms_mqtt_port']
        self.topic = self.cfg['ms_mqtt_tp']

    def start(self):
        if self.using is True:
            mqttClient = mqtt_client.Client(self.clientId)
            mqttClient.username_pw_set(self.username, self.password)
        else:
            mqttClient = mqtt_client.Client()
        mqttClient.on_connect = self.on_connect
        mqttClient.on_disconnect = self.on_disconnect
        mqttClient.on_message = self.on_message
        mqttClient.on_subscribe = self.on_subscribe
        mqttClient.on_unsubscribe = self.on_unsubscribe
        mqttClient.on_publish = self.on_publish
        mqttClient.on_log = self.on_log
        mqttClient.connect(self.host, self.port)
        mqttClient.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.topic)

    def on_disconnect(self, client, userdata, rc):
        print("disconnected with result code " + str(rc))
        pass

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if PayloadProcess.topicIsEqual(msg.topic, self.topic):
            PayloadProcess.process(msg.payload)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        pass

    def on_unsubscribe(self, client, userdata, mid):
        pass

    def on_publish(self, client, userdata, mid):
        pass

    def on_log(self, client, userdata, level, buf):
        pass

