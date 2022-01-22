from deepgram import Deepgram
import asyncio, json

# Your Deepgram API Key
"""
hjel2key
KEY ID:
00658090-ab53-4c4a-b40b-ad695ee42daf
API KEY SECRET:
9e064eb74df1449f432a04deb3ffeb9d26be340b"""


async def main(PATH_TO_FILE, DEEPGRAM_API_KEY):
    # Initialize the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    # Create a websocket connection to Deepgram
    try:
        socket = await dg_client.transcription.live({'punctuate': True})
    except Exception as e:
        print(f'Could not open socket: {e}')
        return

    # Handle sending audio to the socket
    async def process_audio(connection):
        # Open the file
        with open(PATH_TO_FILE, 'rb') as audio:
            # Chunk up the audio to send
            CHUNK_SIZE_BYTES = 8192
            CHUNK_RATE_SEC = 0.001
            chunk = audio.read(CHUNK_SIZE_BYTES)
            while chunk:
                connection.send(chunk)
                await asyncio.sleep(CHUNK_RATE_SEC)
                chunk = audio.read(CHUNK_SIZE_BYTES)

        # Indicate that we've finished sending data
        await connection.finish()

    # Listen for the connection to close
    # socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

    # Print incoming transcription objects
    socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, readintowords)

    # Send the audio to the socket
    await process_audio(socket)


def readintowords(inp: dict):
    global words
    global prevend
    try:
        possibilities = inp['channel']['alternatives']
        if len(possibilities) == 1 and possibilities[0]['transcript'] == '':
            pass
        else:
            maxfound = possibilities[0]['confidence']
            choice = possibilities[0]
            for alternative in possibilities[1:]:
                if alternative['confidence'] > maxfound:
                    choice = alternative
            if prevend >= choice['words'][0]['start']:
                words[-1] = choice
            else:
                prevend = choice['words'][-1]['end']
                words.append(choice)
    except KeyError:
        try:
            inp['transaction_key']
        except:
            raise KeyError('Unexpected KeyError')


def process(path):
    global words
    global prevend
    words = []
    prevend = -1
    key = '9e064eb74df1449f432a04deb3ffeb9d26be340b'
    asyncio.run(main(path, key))
    return words

