import spotipy
import yt_dlp
import os
from spotipy.oauth2 import SpotifyClientCredentials
import time

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def playlist(x):
    if '?' in x:
        s = x[:x.index('?')]
        s = s[-22:]
        return s
    if '/' in x:
        x = x[-22:]     
    return x

# Set up Spotify credentials
def credentials():
    id = input("Input the correct client id, with no spaces. It wont work if its incorrect: ")
    secret = input("Input the correct client secret, with no spaces. It wont work if its incorrect: ")
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(id, secret))
    return sp

def tracklist(play_id, sp):
    offset = 0
    limit = 100
    tracklist = []
    while True:
        try:
            processing = sp.playlist_tracks(play_id, offset=offset, limit=limit)
            
            if len(processing['items']) == 0:
                break  
            
            for item in processing['items']:
                track = item['track']
                if track is not None and track['artists']:
                    tracklist.append(f"{track['name']} - {track['artists'][0]['name']}")
            
            
            offset += limit
            
            time.sleep(2)
        
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)  
    
    print(f'The Amount of songs in this: {len(tracklist)}')

    return tracklist

def download(query):
    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
        search = f'ytsearch:{query}'
        ydl.download([search])

def main():
    # Prompt user for playlist link or ID
    sp = credentials()
    play = playlist(input("Send playlist link or playlist ID: "))
    
    # Create the downloads folder if it doesn't exist
    create_folder('./downloads')
    
    # Get the list of tracks and download each one
    tracks = tracklist(play, sp)
    for track in tracks:
        download(track)

main()
