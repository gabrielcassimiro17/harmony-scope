from spotify.spotify_service import SpotifyManager
import os


# Initialize the SpotifyManager
spotify_manager = SpotifyManager()

# Test function to fetch data for a specific track
def test_fetch_track():
    track_id = '3n3Ppam7vgaVa1iaRUc9Lp'  # Example track ID (Track: "Mr. Brightside" by The Killers)
    track_data = spotify_manager.sp.track(track_id)
    print(f"Track Name: {track_data['name']}")
    print(f"Artist: {track_data['artists'][0]['name']}")
    print(f"Album: {track_data['album']['name']}")

test_fetch_track()
