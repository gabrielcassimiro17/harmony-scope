import pandas as pd


def choose_playlist(spotify_manager):
    playlists = spotify_manager.get_user_playlists()
    for i, playlist in enumerate(playlists["items"]):
        print(f"{i+1}: {playlist['name']}")

    choice = int(input("Enter the number of the playlist you want to analyze: "))
    return playlists["items"][choice - 1]["id"]


def dict_to_dataframe(track_data):
    # Initialize a dictionary to hold the data for DataFrame creation
    df_data = {}

    # Add song name and artist name
    df_data["song_name"] = [track_data["song_name"]]
    df_data["artist_name"] = [track_data["artist_name"]]

    # Add numerical audio features
    for feature, value in track_data["audio_features"].items():
        df_data[feature] = [value]

    # Create a DataFrame
    df = pd.DataFrame(df_data)

    return df


def filter_track_data(track_data):
    # Initialize a new dictionary to hold the filtered data
    filtered_data = {}

    # Extract track information
    track = track_data.get("track", {})
    filtered_data["song_name"] = track.get("name")
    filtered_data["song_popularity"] = track.get("popularity")

    # Extract audio features
    audio_features = track.get("audio_features", {})
    filtered_data["audio_features"] = {
        key: audio_features[key]
        for key in audio_features
        if key not in ["type", "id", "uri", "track_href", "analysis_url"]
    }

    # Extract artist information (assuming first artist)
    artist_info = track.get("artist_info", {})
    filtered_data["artist_name"] = artist_info.get("name")
    filtered_data["artist_popularity"] = artist_info.get("popularity")
    # Include artist genres
    filtered_data["artist_genres"] = artist_info.get("genres", [])

    # Extract album information
    album_info = track.get("album_info", {})
    filtered_data["album_release_date"] = album_info.get("release_date")
    filtered_data["album_popularity"] = album_info.get("popularity")

    return filtered_data
