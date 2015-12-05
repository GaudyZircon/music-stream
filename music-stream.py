import urllib.request
import subprocess

LIMIT = 10
PLAYER = 'vlc'
url = 'http://streams.twitch.tv/kraken/streams?limit='+str(LIMIT)+'&offset=0&game=Music&broadcaster_language=&on_site=1'

with urllib.request.urlopen(url) as response:
    html = response.read().decode('utf8')

i = 0
urls = []
for line in html.split(','):
    if 'status' in line:
        status = line.split('"')[-2]
        status = ''.join(i for i in status if ord(i)<128) #filter non ascii characters
    if 'display_name' in line:
        name = line.split('"')[-2]
        print(str(i) + ') ' + name + ' : ' + status)
        i += 1
    if 'url' in line:
        url = line.split('"')[-2]
        urls.append(url)

choice = LIMIT
while (choice >= LIMIT):
    choice = int(input('Choose a stream\n'))

cmd = ['livestreamer', urls[choice], 'audio']
if PLAYER != 'vlc':
    cmd.append('-p')
    cmd.append(PLAYER)

subprocess.Popen(cmd, shell=False)