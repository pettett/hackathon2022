from deepgram import Deepgram
import asyncio, json
import config

pathfast = "C:/Users/hjela/OneDrive/Documents/NotUni/Hackathon/hackathon2022/lifemovesfast.wav"
pathflorist = "C:/Users/hjela/OneDrive/Documents/NotUni/Hackathon/hackathon2022/florist.mp3"
pathtypog = "C:/Users/hjela/OneDrive/Documents/NotUni/Hackathon/hackathon2022/typographical.webm"
pathplasm = "C:/Users/hjela/OneDrive/Documents/NotUni/Hackathon/hackathon2022/plasmo.webm"


async def main(PATH_TO_FILE, DEEPGRAM_API_KEY):
    # Initialize the Deepgram SDK
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    # Create a websocket connection to Deepgram
    try:
        socket = await dg_client.transcription.live({'punctuate': True, 'multichannel': True})
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
    socket.registerHandler(socket.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

    # Print incoming transcription objects
    socket.registerHandler(socket.event.TRANSCRIPT_RECEIVED, readintowords)

    # Send the audio to the socket
    await process_audio(socket)


def readintowords(inp: dict):
    global words
    global prev
    try:
        possibilities = inp['channel']['alternatives']
        if len(possibilities) == 1 and possibilities[0]['transcript'] == '':
            pass
        else:
            maxfound = possibilities[0]['confidence']
            choice = {'transcript': possibilities[0]['transcript'],
                              'words': [word['word'] for word in possibilities[0]['words']],
                              'start': possibilities[0]['words'][0]['start'],
                              'end': possibilities[0]['words'][-1]['end']}
            for alternative in possibilities[1:]:
                if alternative['confidence'] > maxfound:
                    choice = {'transcript': alternative['transcript'],
                              'words': [word['word'] for word in alternative['words']],
                              'start': alternative['words'][0]['start'],
                              'end': alternative['words'][-1]['end']}
            if not prev:
                words.append(choice)
                prev = choice
            elif prev['end'] > choice['end']:
                prev = choice
                words[-1] = choice
            else:
                changed = True
                script = choice['words']
                prescript = prev['words']
                if len(prescript) < len(script) and contains(prescript, script):
                    words[-1] = choice
                elif contains(script, prescript):
                    changed = False
                else:
                    totlen = min(len(script), len(prescript))
                    different = differences(script, prescript)
                    if different / totlen < 0.7:
                        words[-1] = choice
                    else:
                        words.append(choice)
                if changed:
                    prev = choice
    except KeyError:
        inp['transaction_key']


# code this in OCaml!!!
def differences(words1, words2, upperbound=None, acc=0):
    if not upperbound:
        upperbound = min(len(words1), len(words2))
    if upperbound and (upperbound <= acc): return upperbound
    if not (words1 and words2): return acc
    if upperbound and words1[0] == words2[0]:
        t1 = differences(words1[1:], words2[1:], upperbound, acc)
        t2 = differences(words1[1:], words2, min(t1, upperbound), acc + 1)
        t3 = differences(words1, words2[1:], min(t1, t2), acc + 1)
        return min(upperbound, t1, t2, t3)
    elif words1[0] == words2[0]:
        t1 = differences(words1[1:], words2[1:], acc)
        t2 = differences(words1[1:], words2, t1, acc + 1)
        t3 = differences(words1, words2[1:], min(t1, t2), acc + 1)
        return min(t1, t2, t3)
    elif upperbound:
        t1 = differences(words1[1:], words2, upperbound, acc + 1)
        t2 = differences(words1, words2[1:], min(t1, upperbound), acc + 1)
        return min(upperbound, t1, t2)
    else:
        t1 = differences(words1[1:], words2, upperbound, acc + 1)
        t2 = differences(words1, words2[1:], t1, acc + 1)
        return min(t1, t2)


def contains(short, long):
    ls = len(short)
    ll = len(long)
    for i in range(ll - ls):
        if long[i:i + ls] == short: return True
    return False


def process(path):
    global words
    global prev
    words = []
    prev = None
    asyncio.run(main(path, config.getkey()))
    transcript = []
    for each in words:
        transcript.append((each['transcript'], each['start'], each['end']))
    return transcript
