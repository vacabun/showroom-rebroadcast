import threading
import logging
import ffmpeg
import streamlink
import subprocess


def showroom_is_online(room_url_key):
    url = 'https://www.showroom-live.com/r/{room_url_key}'.format(
        room_url_key=room_url_key)
    streams = streamlink.streams(url)
    if not streams:
        return False
    else:
        return True


def showroom_rebroadcast(room_url_key, output):
    url = 'https://www.showroom-live.com/r/{room_url_key}'.format(
        room_url_key=room_url_key)

    stream_quality = "best"
    streams = streamlink.streams(url)
    available_qualities = streams.keys()
    if stream_quality not in available_qualities:
        raise BaseException('stream quality {stream_quality} is not available.'.format(
            stream_quality=stream_quality))
    stream_url = streams[stream_quality].url

    logging.info('Start to rebroadcast. from {stream_url} to {output}'.format(
        stream_url=stream_url, output=output))

    kwargs_dict = {'vcodec': 'copy',
                   'acodec': 'copy',
                   'f': 'flv',
                   'preset': 'veryslow',
                   'bufsize': '512M',
                   'loglevel': 'error',
                   'g': '125',}
    try:
        (
            ffmpeg
            .input(stream_url,re = None)
            .output(output, **kwargs_dict)
            .global_args('-re')
            .run()
        )
    except KeyboardInterrupt:
        try:
            proc.stdin.write('q'.encode('utf-8'))
        except:
            pass
    except BaseException as e:
        raise e


class Rebroadcaster:
    def __init__(self, room_url_key, output, settings):
        self.room_url_key = room_url_key

        self.output = output
        self.settings = settings
        self.isbroadcast = False
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self.rebroadcast)
        self._thread.daemon = True
        self._thread.start()

    def rebroadcast(self):
        self.isbroadcast = True
        logging.info('{room_url_key}: is on live, start rebroadcast.'.format(
            room_url_key=self.room_url_key))
        try:
            showroom_rebroadcast(self.room_url_key, self.output)
        except BaseException as e:
            self.isbroadcast = False
            logging.error('{room_url_key}: rebroadcast error: {error}'.format(
                room_url_key=self.room_url_key, error=e))
