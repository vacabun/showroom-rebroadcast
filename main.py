import ffmpeg
import logging
import time
import json
import argparse
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='rebroadcast showroom live stream.')
    parser.add_argument('-i', '--id', help='Only monitor this one showroom id.',
                        metavar='SHOWROOM_ID', dest='sr_id')
    parser.add_argument('-o', '--output_url', help='Target RTMP address。',
                        metavar='OUTPUT_URL', dest='output_url')

    args = parser.parse_args()

    if (args.sr_id == None):
        print('Please input a showroom id.')
        exit(1)
    if (args.output_url == None):
        print('Please input a output url.')
        exit(1)

    room_url_key = args.sr_id
    output = args.output_url

    room_id = showroom_get_roomid_by_room_url_key(room_url_key)

    while True:
        timestamp = str(int(time.time() * 1000))
        api_endpoint = 'https://www.showroom-live.com/api/live/streaming_url?room_id={room_id}&_={timestamp}'.format(
            room_id=room_id, timestamp=timestamp)
        html = get_content(api_endpoint)
        html = json.loads(html)
        if len(html) >= 1:
            break
        logging.warning('The live show is currently offline.')
        time.sleep(1)

    stream_url = [i['url'] for i in html['streaming_url_list']
                  if i['is_default'] and i['type'] == 'hls'][0]

    logging.info('The live show is currently online.')
    logging.debug('Start to rebroadcast. from {stream_url} to {output}'.format(
        stream_url=stream_url, output=output))

    kwargs_dict = {'vcodec': 'libx264',
                   'acodec': 'aac',
                   'maxrate': '1.2M',
                   'b:v': '1M',
                   'b:a': '128k',
                   'aac_coder': 'twoloop',
                   'f': 'flv',
                   'preset': 'ultrafast',
                   'bufsize': '256M',
                   'loglevel': 'error',
                   'g': '125',}
    try:
        proc = (
            ffmpeg
            .input(stream_url,re=None)
            .output(output, **kwargs_dict)
            .run()
        )
    except KeyboardInterrupt:
        try:
            proc.stdin.write('q'.encode('utf-8'))
        except:
            pass
