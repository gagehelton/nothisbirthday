#!/usr/bin/python3.8
import os
import json
import logging
import time
from signalwire.relay.consumer import Consumer

messages = open("./messages","r").readlines()

class CustomConsumer(Consumer):
  def setup(self):
    self.project = os.environ['SWproject']
    self.token = os.environ['SWtoken']
    self.contexts = ['office']

  async def ready(self):
    i=-1
    for number in json.loads(os.environ['SWnumbers']):
        i+=1
        if(i>15):
            i=0
        result = await self.client.messaging.send(context='office', 
                    to_number=os.environ['SWtarget'], 
                    from_number=number, 
                    body=messages[i].replace("\n",""))
        if result.successful:
          logging.info(f'Message sent. ID: {result.message_id}')
        time.sleep(.5)

consumer = CustomConsumer()
consumer.run()
