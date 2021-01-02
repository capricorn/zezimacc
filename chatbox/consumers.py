import json
import datetime

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import redis

'''
What we need:
    - A producer that waits for messages from a producer itself (the bot client)
    - and then forwards them to the connected client
'''

# This consumer runs on connection from client
# Server side code
class ChatConsumer(WebsocketConsumer):

    def connect(self):
        print('got connection')

        self.redis = redis.StrictRedis(host='localhost', port='6379', db=0)

        async_to_sync(self.channel_layer.group_add)('chatbox', self.channel_name)
        self.accept()

        '''
        self.send(text_data=json.dumps({
            'message': 'hello'
        }))
        '''

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        #self.send(text_data)
        # broadcast to everyone

        print('got: ' + text_data)
        msg = json.loads(text_data)
        # Parse datetime here
        msg['timestamp'] = msg['timestamp'][:-3] + '.' + msg['timestamp'][-3:]
        print(msg['timestamp'])
        ts = datetime.datetime.fromtimestamp(float(msg['timestamp']))

        self.redis.set(msg['timestamp'], json.dumps({'username': msg['username'], 'message': msg['message']}))

        async_to_sync(get_channel_layer().group_send)('chatbox', {'type': 'test', 
            'timestamp': ts.strftime('%H:%M:%S'), 
            'username': msg['username'],
            'message': msg['message']})

    # Gets sent to every websocket client in group chatbox
    def test(self, event):
        print('hello: ' + str(event))
        #self.send('!!')
        self.send(json.dumps(event))

    # Function called according to type
    def websocket(self, event):
        print('forwarding: ' + str(event))
        async_to_sync(get_channel_layer().group_send)('chatbox', {'type': 'websocket', 'message': 'hello'})

# Connect to this from bot client, send messages which are forwarded to the chatbox
# group
class ChatProducer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # Simply wait for a message from the channel, and forward it to the client?
        print(text_data)


