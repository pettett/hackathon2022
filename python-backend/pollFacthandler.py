
import json 
from text_parser import poll_facts
from navHandler import url_to_identifier
from utils.json import EnhancedJSONEncoder

async def poll_fact_handler(url, timestamp):
    try:
        videoname = url_to_identifier(url)
    except:
        return

    data = poll_facts(videoname,timestamp)
    return json.dumps({
        "type": "facts",
        "data": json.dumps(data, cls=EnhancedJSONEncoder)
    })