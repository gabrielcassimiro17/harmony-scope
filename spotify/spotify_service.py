import os
import spotipy
from dotenv import find_dotenv, load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

load_dotenv(find_dotenv())

class SpotifyManager:
    def __init__(self, scope="playlist-read-private user-read-playback-state"):
        self.oauth = SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID") or st.secrets["SPOTIPY_CLIENT_ID"],
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET") or st.secrets["SPOTIPY_CLIENT_SECRET"],
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI") or st.secrets["SPOTIPY_REDIRECT_URI"],
            scope=scope,
            cache_path=None  # This ensures we don't use a physical file for caching
        )
        self.sp = None  # Initialize Spotify client as None

    def authenticate_user(self):
        """Handles the process of authenticating the user."""
        try:
            # Check if we already have a valid token in the session
            if "token_info" in st.session_state:
                self.sp = spotipy.Spotify(auth=st.session_state["token_info"])

            else:
                # Attempt to authenticate the user and get a new token
                query_params = st.query_params
                code = query_params.get("code")
                if code:
                    token_info = self.oauth.get_access_token(code, as_dict=False, check_cache=False)
                    if token_info:
                        st.session_state["token_info"] = token_info
                        self.sp = spotipy.Spotify(auth=token_info)
                    else:
                        st.error("Failed to authenticate with Spotify.")
                else:
                    # Redirect user for authentication if no code is present
                    self.redirect_for_authentication()
        except Exception as e:
            st.write("An error occured on you log in. Please Refresh and try again")
            self.clear_cache()

    def redirect_for_authentication(self):
        """Redirects the user to the Spotify authentication URL."""
        auth_url = self.oauth.get_authorize_url()
        st.markdown(f"[Log in to Spotify]({auth_url})", unsafe_allow_html=True)

    def clear_cache(self):
        """Clears any authentication tokens from the session."""
        if "token_info" in st.session_state:
            del st.session_state["token_info"]

    def get_currently_playing(self):
        """Fetches the currently playing track, if any."""
        return self.sp.current_playback()

    def get_user_playlists(self):
        """Fetches all user playlists."""
        playlists = []
        results = self.sp.current_user_playlists(limit=50)
        playlists.extend(results["items"])
        while results["next"]:
            results = self.sp.next(results)
            playlists.extend(results["items"])
        return playlists

    def get_playlist_by_id(self, playlist_id):
        """Fetches a specific playlist by its ID."""
        return self.sp.playlist(playlist_id)

    def get_tracks_from_playlist(self, playlist_id, max_songs=500):
        """Fetches up to max_songs tracks from the specified playlist."""
        tracks = []
        results = self.sp.playlist_items(playlist_id)
        tracks.extend(results["items"])

        while results["next"] and len(tracks) < max_songs:
            results = self.sp.next(results)
            tracks.extend(results["items"])
            # If we have fetched max_songs, truncate the list of tracks
            if len(tracks) >= max_songs:
                tracks = tracks[:max_songs]
                break

        return tracks

    def get_audio_features_for_tracks(self, track_ids):
        """Fetches audio features for given track IDs."""
        audio_features = []
        # Spotify limits the number of track IDs that can be requested at once, so we may need to batch
        batch_size = 100
        for i in range(0, len(track_ids), batch_size):
            batch_ids = track_ids[i : i + batch_size]
            audio_features += self.sp.audio_features(batch_ids)
        return audio_features

    def get_artist_features_for_tracks(self, artist_ids):
        """Fetches artist information in batches for given artist IDs."""
        artist_features = {}
        batch_size = 50  # Spotify API limit for artist batch requests
        for i in range(0, len(artist_ids), batch_size):
            batch_ids = artist_ids[i : i + batch_size]
            artists_data = self.sp.artists(batch_ids)["artists"]
            for artist in artists_data:
                artist_features[artist["id"]] = artist
        return artist_features

    def get_album_features_for_tracks(self, album_ids):
        """Fetches album information in batches for given album IDs."""
        album_features = {}
        batch_size = (
            20  # Adjust the batch size as needed, considering the API's rate limits
        )
        for i in range(0, len(album_ids), batch_size):
            batch_ids = album_ids[i : i + batch_size]
            albums_data = self.sp.albums(batch_ids)["albums"]
            for album in albums_data:
                album_features[album["id"]] = album
        return album_features

    def get_full_track_data(self, playlist_id):
        # Fetch tracks metadata
        tracks_metadata = self.get_tracks_from_playlist(playlist_id)

        # Extract track IDs
        track_ids = [
            item["track"]["id"]
            for item in tracks_metadata
            if item.get("track", {}).get("id")
        ]

        # Fetch audio features for these track IDs
        audio_features_list = self.get_audio_features_for_tracks(track_ids)

        # Convert list of audio features to a dictionary for easier access
        audio_features_dict = {af["id"]: af for af in audio_features_list if af}

        # Fetch artist and album data in batches
        artist_ids = [
            track["track"]["artists"][0]["id"]
            for track in tracks_metadata
            if track.get("track", {}).get("artists")
        ]
        album_ids = [
            track["track"]["album"]["id"]
            for track in tracks_metadata
            if track.get("track", {}).get("album")
        ]

        artist_features = self.get_artist_features_for_tracks(artist_ids)
        album_features = self.get_album_features_for_tracks(album_ids)

        # Map audio features, artist features, and album features to their respective tracks
        for item in tracks_metadata:
            track = item["track"]
            track_id = track["id"]
            artist_id = track["artists"][0]["id"]
            album_id = track["album"]["id"]

            # Map audio features
            track["audio_features"] = audio_features_dict.get(track_id, {})

            # Map artist and album information
            track["artist_info"] = artist_features.get(artist_id, {})
            track["album_info"] = album_features.get(album_id, {})

        return tracks_metadata
