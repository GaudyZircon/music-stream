#!/usr/bin/env python3
import urllib.request
import subprocess

LIMIT = 10
CLIENT_ID='jzkbprff40iqj646a697cyrvl0zt2m6'
PLAYER = 'vlc'
STREAMS_URL = 'https://api.twitch.tv/kraken/streams?limit='+str(LIMIT)+'&offset=0&game=Music&broadcaster_language=&on_site=1&client_id='+str(CLIENT_ID)

while True:
    with urllib.request.urlopen(STREAMS_URL) as response:
        html = response.read().decode('utf8')

    i = 0
    urls = []
    for line in html.split(','):
        if 'status' in line:
            status = line.split('"')[-2]
            status = ''.join(i for i in status if ord(i)<128) #filter non ascii characters
        if 'display_name' in line:
            name = line.split('"')[-2]
            name = ''.join(i for i in name if ord(i)<128) #filter non ascii characters
            print(str(i) + ') ' + name + ' : ' + status)
            i += 1
        if 'url' in line:
            url = line.split('"')[-2]
            urls.append(url)

    choice = LIMIT
    while (choice >= LIMIT):
        try:
            choice = int(input('Choose a stream\n'))
        except ValueError:
            pass

    cmd = ['livestreamer', '--http-header', 'Client-ID='+str(CLIENT_ID), urls[choice], 'audio,audio_only']
    if PLAYER != 'vlc':
        cmd.append('-p')
        cmd.append(PLAYER)

    subprocess.call(cmd, shell=False)
    print('\n\n\n')
