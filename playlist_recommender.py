import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import os
import pandas as pd


# Set your Spotify API credentials as environment variables
os.environ["SPOTIPY_CLIENT_ID"] = 'client ID'
os.environ["SPOTIPY_CLIENT_SECRET"] = 'client secret'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost/3630'

sp = sp.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", open_browser=False))


# Function to get track suggestions
def get_track_suggestions(track_name):
    results = sp.search(q=track_name, type='track', limit=10)
    suggestions = [f"{i + 1}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}" for i, track in enumerate(results['tracks']['items'])]
    return suggestions

# Function to create a playlist
def create_playlist(playlist_name, track_uris):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    sp.playlist_add_items(playlist['id'], track_uris)
    return playlist['id']

# Function to generate the Spotify link
def generate_spotify_link(playlist_id):
    return f"https://open.spotify.com/playlist/{playlist_id}"

# Enter a song name to get suggestions
song_name = input("Enter a song name: ")
suggestions = get_track_suggestions(song_name)

# Display suggestions
for suggestion in suggestions:
    print(suggestion)

# Prompt user for song selection
selected_index = int(input("Enter the index of the song you want to create a playlist from: ")) - 1

# Validate the selected index
if 0 <= selected_index < len(suggestions):
    selected_track = suggestions[selected_index]
    print(f"Creating a playlist based on {selected_track}")
    
    # Get track URI of the selected song
    track_uri = sp.search(q=song_name, type='track', limit=1)['tracks']['items'][0]['uri']

    # Get recommended tracks based on the selected song
    recommendations = sp.recommendations(seed_tracks=[track_uri], limit=10)['tracks']

    # Extract track URIs from recommendations
    track_uris = [track['uri'] for track in recommendations]

    # Create a playlist and add recommended tracks
    playlist_name = "Recommended Playlist"
    playlist_id = create_playlist(playlist_name, track_uris)

    # Generate Spotify link
    spotify_link = generate_spotify_link(playlist_id)
    print(f"Playlist '{playlist_name}' created with {len(track_uris)} recommended tracks.")
    print(f"You can access your playlist here: {spotify_link}")
else:
    print("Invalid index. Please select a valid index from the suggestions.")
