import os

def readSettingsFile(filename):
    settingsTxt = """
[settings]
room_url_key =  LOVE_SHOKO_TAKIWAKI                      # room_url_key
sever_url = rtmp://live-push.bilivideo.com/live-bvc/     # target rtmp url
stream_key = 
"""
    # create file if not present
    path = os.getcwd()
    filenamepath = os.path.join(path, filename)
    if not os.path.isfile(filenamepath):
        with open(filenamepath, 'w', encoding='utf8') as fp:
            fp.write(settingsTxt)
        print('Created {}'.format(filename))

    with open(filenamepath, 'r', encoding='utf8') as fp:
        lines = fp.readlines()

    settings = {}

    for line in lines:
        # remove # and line after it
        sharp = line.find('#')
        if sharp > -1:
            line = line[:sharp]
        line = line.strip()
        if len(line) == 0:
            continue

        if line.lower().find('[settings]') > -1:
            continue
        
        s1, s2 = line.split("=", 1)
        settings.update(
            {s1.strip(): s2.strip()})

    return settings
