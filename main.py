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
    full_track_data = spotify_manager.get_full_track_data(playlist_id)

    for track_data in full_track_data:
        track = track_data['track']
        print(f"{track['name']} by {track['artists'][0]['name']}")
        audio_features = track.get('audio_features')
        if audio_features:
            print(f"  - Tempo: {audio_features['tempo']}")
            print(f"  - Key: {audio_features['key']}")
            # Add more features as needed
    print(track_data)
if __name__ == "__main__":
    main()
