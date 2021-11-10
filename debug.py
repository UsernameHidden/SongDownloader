
import pycurl
from io import BytesIO 
import requests
from pytube import YouTube

url = "https://open.spotify.com/playlist/37i9dQZF1DXa0PTjSQ7AeJ?si=4d5ca075090d4925" # input("[+] Spotify URL: ")

b_obj = BytesIO() 
crl = pycurl.Curl() 
crl.setopt(crl.URL, url)
crl.setopt(crl.WRITEDATA, b_obj)
crl.perform() 
crl.close()
get_body = b_obj.getvalue()
body = get_body.decode('utf8')


# number of songs in the playlist
cut_number_of_songs_in_playlist = body[body.index('''<meta property="music:song_count" content="''') + len('''<meta property="music:song_count" content="'''):]
number_of_songs = int(cut_number_of_songs_in_playlist[0]+ cut_number_of_songs_in_playlist[1])
print(f"[+] Number of songs in the playlist: {number_of_songs}")

artist_name = ""
artist_tag = '''This Is '''
artist = body[body.index(artist_tag, body.find(artist_tag)+ len(artist_tag)):] 
for x in range(20):
    artist_name = artist_name + artist[x]
    x = x + 1
    if artist[x] == '"':
        break
try:
    artist_name = artist_name.replace("This Is ", "")
except:
    pass
print(f"[+] Name of the artist: {artist_name}")

#*****************************************************************************************#


target = f'''class="track-name" dir="auto">'''
raw_songs = []
song = ""
counter = -1500 
list_counter = 1

while counter < 46000:

    cut_number_of_songs = body[30 + body.find(target, counter + body.find(target)+ len(target) ):]

    for i in range(1000000):
        song = song + cut_number_of_songs[i]
        i = i + 1 
        if song == '''"''':
            break
        if cut_number_of_songs[i] == "<":
            break
        if cut_number_of_songs[i] == "(":
            break
    raw_songs.append(song)
    song = ""
    counter = counter + 1500

raw_songs = list(dict.fromkeys(raw_songs))

songs = [clean.replace("&#039;", "") for clean in raw_songs]
del songs[-1]

#*****************************************************************************************#

song_links = []

for raw_song in songs:
    song_url = f"https://www.youtube.com/results?search_query={artist_name}+{raw_song}+lyrics".replace(" ", "+").lower()
    x = requests.get(song_url).content.decode("utf-8") 

    vid_link = x[x.index('''"commandMetadata":{"webCommandMetadata":{"url":"/watch?v=''') + len('''"commandMetadata":{"webCommandMetadata":{"url":"/watch?v='''):]
    raw_link = vid_link[0]+ vid_link[1]+ vid_link[2]+ vid_link[3]+ vid_link[4]+ vid_link[5]+ vid_link[6]+ vid_link[7]+ vid_link[8]+ vid_link[9]+ vid_link[10]
    print(f"[+] Link of the video: {raw_link} || {raw_song}")
    song_links.append(raw_link)

print(song_links)

#*****************************************************************************************#
for download, raw_song_name in zip(song_links,songs):

    print("\n[+] Downloading "+ raw_song_name)

    yt = YouTube(f"https://www.youtube.com/watch?v={download}") 

    # accessing audio streams of YouTube obj.(first one, more available)
    stream = yt.streams.filter(only_audio=True).first()
    # downloading a video would be: stream = yt.streams.first() 

    # download into working directory
    stream.download()
    print("[+] "+raw_song_name + " has been downloaded successfully")



