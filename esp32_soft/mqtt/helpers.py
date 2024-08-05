import json

from umqtt.robust import MQTTClient

from heating import handle_heating


class StorageHeaterClient(MQTTClient):

    def setup(self, topic_sub):
        self.set_callback()
        self.connect()
        self.subscribe(topic_sub)
        print('Connected to %s MQTT broker, subscribed to %s topic' % (self.server, topic_sub))

    def set_callback(self):
        self.cb = self.callback()

    def callback(self):
        def callback(topic, msg):
            if msg.startswith('relay'):
                decoded_message = msg.decode('ascii')
                response = handle_heating(decoded_message[8:], int(decoded_message[6]))
                self.publish(topic, json.dumps(response))

        return callback
