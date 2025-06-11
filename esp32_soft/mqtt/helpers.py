import json

from robust2 import MQTTClient

from heating import handle_heating



class StorageHeaterClient(MQTTClient):

    def setup(self, topic_sub):
        self.set_callback(self.callback())
        self.connect()
        self.subscribe(topic_sub)
        print('Connected to %s MQTT broker, subscribed to %s topic' % (self.server, topic_sub))

    @staticmethod
    def callback():
        def callback(topic, msg, retained, duplicate):
            if msg:
                data = json.loads(msg)
                if data and data.get('heating_action'):
                    message = data['heating_action']
                    #  decoded_message = msg.decode('ascii')
                    response = handle_heating(message[8:], int(message[6]))
                    print(response)

        return callback
