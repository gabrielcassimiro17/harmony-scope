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


    def get_full_track_data(self, playlist_id):
        tracks_metadata = self.get_tracks_from_playlist(playlist_id)

        # Extract the first artist ID from each track
        artist_ids = [track['track']['artists'][0]['id'] for track in tracks_metadata if 'track' in track and track['track']['artists']]

        # Fetch artist data in batches
        artist_features = self.get_artist_features_for_tracks(artist_ids)

        # Map audio features and artist features to their respective tracks
        for track in tracks_metadata:
            track_id = track['track']['id']
            artist_id = track['track']['artists'][0]['id']
            track['track']['artist_info'] = artist_features.get(artist_id)

        return tracks_metadata

    # def get_full_track_data(self, playlist_id):
    #     """Fetches all tracks with metadata and audio features from the specified playlist."""
    #     tracks_metadata = self.get_tracks_from_playlist(playlist_id)

    #     # Extract track IDs
    #     track_ids = [track['track']['id'] for track in tracks_metadata if 'track' in track and 'id' in track['track']]


    #     # Fetch audio features for these track IDs
    #     audio_features_list = self.get_audio_features_for_tracks(track_ids)
    #     artist_features_list = self.get_artist_features_for_tracks(track_ids)

    #     # Map audio features to their respective tracks
    #     for i, track in enumerate(tracks_metadata):
    #         track_id = track['track']['id']
    #         # Find the corresponding audio features based on track ID
    #         track['track']['audio_features'] = next((af for af in audio_features_list if af and af['id'] == track_id), None)
    #         #Find the corresponding artist features based on track ID
    #         ####TODO

    #     return tracks_metadata
