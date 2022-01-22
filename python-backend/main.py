import asyncio
import websockets

async def run(websocket, path):
    counter = 1
    while True:
        counter+=1
        await websocket.send(str(counter))
        await asyncio.sleep(1)

if __name__ == "__main__":
    start_server = websockets.serve(run, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()