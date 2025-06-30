import json

from helpers import log_over_mqtt
from robust2 import MQTTClient

from heating import handle_heating



class Client(MQTTClient):

    def setup(self, topic_sub):
        self.DEBUG = True
        self.KEEP_QOS0 = False
        self.NO_QUEUE_DUPS = True
        self.MSG_QUEUE_MAX = 2

        self.set_callback(self.callback)

        if not self.connect(clean_session=True):
            self.subscribe(topic_sub)
        print('Connected to %s MQTT broker, subscribed to %s topic' % (self.server, topic_sub))

    @staticmethod
    def callback(topic, msg, retained, duplicate):
        if msg:
            try:
                data = json.loads(msg)
            except json.decoder.JSONDecodeError as error:
                log_over_mqtt(error)
                return

            if data and data.get('heating_action'):
                message = data['heating_action']
                #  decoded_message = msg.decode('ascii')
                response = handle_heating(message[8:], int(message[6]))
                print(response)




    def check_and_restore_mqtt(self):
        if self.is_conn_issue():
            while self.is_conn_issue():
                self.reconnect()
            else:
                self.resubscribe()

