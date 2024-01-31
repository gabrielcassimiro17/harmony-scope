import os
import spotipy
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(find_dotenv())



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

    def get_audio_features_for_tracks(self, track_ids):
        """Fetches audio features for given track IDs."""
        audio_features = []
        # Spotify limits the number of track IDs that can be requested at once, so we may need to batch
        batch_size = 100
        for i in range(0, len(track_ids), batch_size):
            batch_ids = track_ids[i:i+batch_size]
            audio_features += self.sp.audio_features(batch_ids)
        return audio_features

    def get_artist_features_for_tracks(self, artist_ids):
        """Fetches artist information in batches for given artist IDs."""
        artist_features = {}
        batch_size = 50  # Spotify API limit for artist batch requests
        for i in range(0, len(artist_ids), batch_size):
            batch_ids = artist_ids[i:i + batch_size]
            artists_data = self.sp.artists(batch_ids)['artists']
            for artist in artists_data:
                artist_features[artist['id']] = artist
        return artist_features

    def get_album_features_for_tracks(self, album_ids):
        """Fetches album information in batches for given album IDs."""
        album_features = {}
        batch_size = 20  # Adjust the batch size as needed, considering the API's rate limits
        for i in range(0, len(album_ids), batch_size):
            batch_ids = album_ids[i:i + batch_size]
            albums_data = self.sp.albums(batch_ids)['albums']
            for album in albums_data:
                album_features[album['id']] = album
        return album_features

    def get_full_track_data(self, playlist_id):
        tracks_metadata = self.get_tracks_from_playlist(playlist_id)

        # Extract artist and album IDs from each track
        artist_ids = [track['track']['artists'][0]['id'] for track in tracks_metadata if 'track' in track and track['track']['artists']]
        album_ids = [track['track']['album']['id'] for track in tracks_metadata if 'track' in track and 'album' in track['track']]

        # Fetch artist and album data in batches
        artist_features = self.get_artist_features_for_tracks(artist_ids)
        album_features = self.get_album_features_for_tracks(album_ids)

        # Map artist and album features to their respective tracks
        for track in tracks_metadata:
            artist_id = track['track']['artists'][0]['id']
            album_id = track['track']['album']['id']
            track['track']['artist_info'] = artist_features.get(artist_id)
            track['track']['album_info'] = album_features.get(album_id)

        return tracks_metadata
