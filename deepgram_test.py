from deepgram import Deepgram
import asyncio
import config


async def main(PATH_TO_FILE):
    global jsonstore
    dg_client = Deepgram(config.getkey())
    with open(PATH_TO_FILE, 'rb') as audio: return await dg_client.transcription.prerecorded({'buffer': audio, 'mimetype': 'audio/wav'}, {'punctuate': True})


def process(path):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    response = asyncio.run(main(path))['results']['channels'][0]['alternatives']
    mle, ml = -1, None
    for alternative in response:
        if alternative['confidence'] > mle: ml, mle = alternative, alternative['confidence']
    return ml['transcript'], [(word['word'], word['start'], word['end']) for word in ml['words'] if word['confidence'] > 0.6]
