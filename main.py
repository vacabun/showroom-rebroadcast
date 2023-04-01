import ffmpeg
import logging
import time
import json
from you_get.common import get_content, match1
def showroom_get_roomid_by_room_url_key(room_url_key):
    """str->str"""
    fake_headers_mobile = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'UTF-8,*;q=0.5',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
    }
    webpage_url = 'https://www.showroom-live.com/' + room_url_key
    html = get_content(webpage_url, headers=fake_headers_mobile)
    roomid = match1(html, r'room\?room_id\=(\d+)')
    assert roomid
    return roomid

room_url_key = 'ME_HANA_OGI'

room_id = showroom_get_roomid_by_room_url_key(room_url_key)
while True:
    timestamp = str(int(time.time() * 1000))
    api_endpoint = 'https://www.showroom-live.com/api/live/streaming_url?room_id={room_id}&_={timestamp}'.format(
        room_id=room_id, timestamp=timestamp)
    html = get_content(api_endpoint)
    html = json.loads(html)
    if len(html) >= 1:
        break
    logging.w('The live show is currently offline.')
    time.sleep(1)

stream_url = [i['url'] for i in html['streaming_url_list']
              if i['is_default'] and i['type'] == 'hls'][0]

output = 'rtmp://live-push.bilivideo.com/live-bvc/?streamname=live_12814697_5336514&key=acd42d735baaad7951e71d5a9e3a2017&schedule=rtmp&pflag=1'
(
    ffmpeg
    .input(stream_url)
    .output(output, **{'vcodec': 'copy', 'acodec': 'copy', 'f': 'flv', 'bufsize': '3000k'})
    .global_args("-re")
    .run()
)
