import json
from channels.generic.websocket import WebsocketConsumer
from .models import GroupMessage, ChatGroup
from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        # Get the room name from the URL route
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', 'public2')
        self.room_group_name = self.room_name
        
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

    def receive(self, text_data):
        try:
            print(f"Received message in room {self.room_group_name}: {text_data}")  # Debug print
            data = json.loads(text_data)
            # Extract message from HTMX format
            message = data.get('message', '')
            if not message and 'HEADERS' in data:
                # If message is empty, try to get it from form data
                form_data = {k: v for k, v in data.items() if k != 'HEADERS'}
                message = form_data.get('message', '')
            
            if message:
                try:
                    # Save to database
                    chat_group = ChatGroup.objects.get(group_name=self.room_group_name)
                    chat_message = GroupMessage.objects.create(
                        author=self.scope["user"],
                        body=message,
                        group=chat_group
                    )
                    
                    # Send message to room group
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'username': self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"
                        }
                    )
                except ObjectDoesNotExist:
                    print(f"Error: ChatGroup 'public2' does not exist")
                except Exception as e:
                    print(f"Error saving message to database: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Error in receive: {e}")

    def chat_message(self, event):
        # Send message to WebSocket
        message = event['message']
        username = event['username']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room_name': self.room_group_name
        }))