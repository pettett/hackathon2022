import asyncio
from copyreg import constructor
from email import message
import websockets
import json
import navHandler as navHandler
import pollFacthandler as pollFacthandler
async def consumer(message):
    #Message format is 
    # { "type": message_type
    #   "data": 
    # }
    message_parsed = json.loads(message)
    message_type = message_parsed['type']
    message_data = message_parsed['data']
    print(message)
    if message_type == "navChange":
        await navHandler.nav_handler(message_data['url'])
    elif message_type == "echo":
        print(message_data)
    elif message_type == "pollFact":
        return await pollFacthandler.poll_fact_handler(message_data['url'], message_data['timestamp'])
    

async def consumer_handler(websocket, path):
    async for message in websocket:
        response = await consumer(message)
        if response is not None:
            await websocket.send(response)

async def handler(websocket, path):
    await asyncio.gather(
        consumer_handler(websocket, path),
        #producer_handler(websocket, path),
    )

async def producer():
    counter = 1
    while True:
        counter+=1
        await asyncio.sleep(1)
        yield str(counter)

#async def producer_handler(websocket, path):
 #   while True:
        #ADD AWAIT
        #message = await producer()
  #      message="magic"
   #     await asyncio.sleep(1)
    #    await websocket.send(message)


if __name__ == "__main__":
    start_server = websockets.serve(handler, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()