# call/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer

clients = []

channel_layer = get_channel_layer()


class CallConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.my_name = None

    def connect(self):

        # channel_name = self.scope['url_route']['kwargs']['username']
        # print(channel_name)
        # self.my_name = channel_name

        print("NEW CONNECT")

        self.accept()

        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.my_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("WEBSOCKET-MESSAGE", text_data_json)

        eventType = text_data_json['type']

        if eventType == 'login':
            name = text_data_json['data']['name']

            self.my_name = name

            print("LOGIN")

            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )

            self.send(text_data=json.dumps({
                'type': 'websocket.accept',
                'data': {
                    'message': 'TEST'
                }
            }))

            # self.send(text_data=json.dumps({
            #     'type': 'login',
            #     'data': {
            #         'message': 'TEST'
            #     }
            # }))
            #
            # async_to_sync(self.channel_layer.group_send)(
            #     self.my_name,
            #     {
            #         'type': 'login',
            #         'data': {
            #             'message': "Connected 222222222222222222222222"
            #         }
            #     }
            # )

        if eventType == 'call':
            name = text_data_json['data']['name']
            print(self.my_name, "is calling", name)

            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'call_received',
                    'data': {
                        'caller': self.my_name,
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'answer_call':

            caller = text_data_json['data']['caller']

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'call_answered',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'ICEcandidate':
            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'ICEcandidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if eventType == 'a':
            user = text_data_json['data']['user_registrant_username']
            print(user)
            async_to_sync(self.channel_layer.group_send)(
                "group",
                {
                    'type': 'connection',
                    'data': {
                        'user_id': text_data_json['data']['user_id'],
                        'username': text_data_json['data']['username'],
                        'user_email': text_data_json['data']['user_email'],
                    }
                }
            )

    def call_received(self, event):

        # print(event)
        print('Call received by ', self.my_name)
        self.send(text_data=json.dumps({
            'type': 'call_received',
            'data': event['data']
        }))

    def call_answered(self, event):

        # print(event)
        print(self.my_name, "'s call answered")
        self.send(text_data=json.dumps({
            'type': 'call_answered',
            'data': event['data']
        }))

    def ICEcandidate(self, event):
        self.send(text_data=json.dumps({
            'type': 'ICEcandidate',
            'data': event['data']
        }))
