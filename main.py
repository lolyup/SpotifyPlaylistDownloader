import spotipy
import yt_dlp
import os
from spotipy.oauth2 import SpotifyClientCredentials

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
id = input("Enter correct user id from spotify developer portal(code will fail if its wrong): ")
secret = input("Enter correct client secret from spotify developer portal(code will fail if its wrong): ")
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(id, secret))

def tracklist(play_id):
    processing = sp.playlist_tracks(play_id)
    tracklist = []
    for item in processing['items']:
        track = item['track']
        tracklist.append(f"{track['name']} - {track['artists'][0]['name']}")
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
    play = playlist(input("Send playlist link or playlist ID: "))
    
    # Create the downloads folder if it doesn't exist
    create_folder('./downloads')
    
    # Get the list of tracks and download each one
    tracks = tracklist(play)
    for track in tracks:
        download(track)

if __name__ == "__main__":
    main()
