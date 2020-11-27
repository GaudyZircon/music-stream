#!/usr/bin/env python3
import urllib.request
import urllib.parse
import subprocess

LIMIT = 20
CLIENT_ID='jzkbprff40iqj646a697cyrvl0zt2m6'
PLAYER = 'vlc'
GAMES = ['Music', 'Music%20%26%20Performing%20Arts']

while True:
    i = 0
    for game in GAMES:
        print(str(i) + ') ' + urllib.parse.unquote(game))
        i += 1

    choice = len(GAMES)
    while (choice >= len(GAMES)):
        try:
            choice = int(input('Choose a playlist\n'))
        except ValueError:
            pass
    print('\n')

    game = GAMES[choice]
    streams_url = 'https://api.twitch.tv/kraken/streams?limit='+str(LIMIT)+'&offset=0&game='+game
    req = urllib.request.Request(streams_url)
    req.add_header('Accept', 'application/vnd.twitchtv.v5+json')
    req.add_header('Client-ID', CLIENT_ID)
    html = None
    with urllib.request.urlopen(req) as response:
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

    cmd = ['streamlink', '--http-header', 'Client-ID='+str(CLIENT_ID), urls[choice], 'audio,audio_only', '--twitch-disable-ads']
    if PLAYER != 'vlc':
        cmd.append('-p')
        cmd.append(PLAYER)

    subprocess.call(cmd, shell=False)
    print('\n\n\n')
