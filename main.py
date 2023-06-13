import logging
import argparse
import config
import rebroadcast
import time


if __name__ == "__main__":
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleFmt = logging.Formatter(
        fmt='%(asctime)s %(message)s', datefmt='%H:%M:%S')
    consoleHandler.setFormatter(consoleFmt)
    consoleHandler.setLevel(logging.DEBUG)
    log.addHandler(consoleHandler)

    parser = argparse.ArgumentParser(
        description='rebroadcast showroom live stream.')
    parser.add_argument('-i', '--id', help='Only monitor this one showroom id.',
                        metavar='SHOWROOM_ID', dest='sr_id')
    parser.add_argument('-o', '--output_url', help='Target RTMP address。',
                        metavar='OUTPUT_URL', dest='output_url')

    args = parser.parse_args()

    settings = config.readSettingsFile('config.ini')

    if args.sr_id is None:
        room_url_key = settings['room_url_key']
    else:
        room_url_key = args.sr_id

    if args.output_url is None:
        output = settings['sever_url'] + settings['stream_key']
    else:
        output = args.output_url

    rb = rebroadcast.Rebroadcaster(room_url_key, output, None)

    while True:
        try:
            if rb.isbroadcast is False:
                if rebroadcast.showroom_is_online(room_url_key):
                    rb.start()
            time.sleep(30)
        except KeyboardInterrupt:
            logging.info("bye")
            break
        except Exception as e:
            logging.error(e)
