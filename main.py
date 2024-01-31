from spotify.spotify_service import SpotifyManager
import os

def choose_playlist(spotify_manager):
    playlists = spotify_manager.get_user_playlists()
    for i, playlist in enumerate(playlists['items']):
        print(f"{i+1}: {playlist['name']}")

    choice = int(input("Enter the number of the playlist you want to analyze: "))
    return playlists['items'][choice - 1]['id']

def main():
    spotify_manager = SpotifyManager()
    playlist_id = choose_playlist(spotify_manager)
    tracks = spotify_manager.get_tracks_from_playlist(playlist_id)

    for track in tracks:
        track_info = track['track']
        print(f"{track_info['name']} by {track_info['artists'][0]['name']}")

if __name__ == "__main__":
    main()
