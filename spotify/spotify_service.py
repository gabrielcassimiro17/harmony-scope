import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

class SpotifyManager:
    def __init__(self):
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

        if not client_id or not client_secret:
            raise Exception("Spotify client ID and secret must be set as environment variables")

        self.client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
