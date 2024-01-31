import os
import spotipy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

# class SpotifyManager:
#     def __init__(self):
#         client_id = os.getenv('SPOTIPY_CLIENT_ID')
#         client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

#         if not client_id or not client_secret:
#             raise Exception("Spotify client ID and secret must be set as environment variables")

#         self.client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#         self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyManager:
    def __init__(self, scope="playlist-read-private"):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            scope=scope
        ))

    def get_user_playlists(self):
        """Fetches a list of the user's playlists."""
        return self.sp.current_user_playlists()

    def get_playlist_by_id(self, playlist_id):
        """Fetches a specific playlist by its ID."""
        return self.sp.playlist(playlist_id)

    def get_tracks_from_playlist(self, playlist_id):
        """Fetches all tracks from the specified playlist."""
        tracks = []
        results = self.sp.playlist_items(playlist_id)
        tracks.extend(results['items'])

        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])

        return tracks
