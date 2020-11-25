# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from .models import serh,todo
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from django.contrib.auth.models import User



class ChatConsumer(WebsocketConsumer):
    


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        message  = data['message']
        author   = data['author']
        todo_    = data['todo']

        todom = todo.objects.get(id = int(todo_))
        userim   = User.objects.get(username=author)
        serh.objects.create(metin=message,useri=userim,todom=todom) 
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author':author,
                'todo':todo_,
               
            }
            
        )
       
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        author  = event['author']
        

        # Send message to WebSocket
        async_to_sync(self.send(text_data=json.dumps({
            'message': message,
            'author':author,

        })))


    
 