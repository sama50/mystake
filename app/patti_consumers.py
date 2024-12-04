import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer 
from asgiref.sync import async_to_sync 
from django.contrib.auth.models import User
from time import sleep
import datetime
from channels.db import database_sync_to_async

from app.services import check_and_start_game, stop_game



class PattiConsumers(AsyncJsonWebsocketConsumer):
    count = 0
    async def connect(self):
        await self.accept() 
        print("USER ::: CONNECTED")
        self.ansside = None
        await self.channel_layer.group_add(f"patti", self.channel_name)
        await database_sync_to_async(check_and_start_game)()
 
         
         
    async def disconnect(self, close_code): 
        await database_sync_to_async(stop_game)()
         


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        print(text_data)
        if text_data.get('eventname') == 'ansimage':
            self.ansside = text_data.get('cardside',None)
 
    async def send_msg(self,event):
        print(event['msg'])
        await self.send_json(event["msg"])

    async def start_game(self,event):
        await self.send_json(event["data"])
    
    async def send_card_side_event(self,event):
        await self.send_json(event["data"])
         
    async def send_winner(self,event):
        if self.ansside:
            event["data"]["is_you_win"] = "WIN" if self.ansside == event["data"]["side"] else "LOSS"

        event["data"]["is_you_win"] = "NO SELECT"
        await self.send_json(event["data"])