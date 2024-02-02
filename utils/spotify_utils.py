import pandas as pd
import streamlit as st

def choose_playlist(spotify_manager):
    playlists = spotify_manager.get_user_playlists()
    for i, playlist in enumerate(playlists["items"]):
        print(f"{i+1}: {playlist['name']}")

    choice = int(input("Enter the number of the playlist you want to analyze: "))
    return playlists["items"][choice - 1]["id"]

def select_playlist_streamlit(spotify_manager):
    playlists = spotify_manager.get_user_playlists()
    playlist_names = [playlist['name'] for playlist in playlists]  # Directly iterating over playlists list

    # Use Streamlit's selectbox for user selection
    selected_playlist = st.sidebar.selectbox("Select a Playlist:", playlist_names)

    # Find the selected playlist details
    selected_playlist_details = next((playlist for playlist in playlists if playlist['name'] == selected_playlist), None)
    container_style = """
    <style>
    .spotify-green-container {
        background-color: #1DB954; /* Spotify Green */
        color: white;
        padding: 5px 10px; /* Reduced vertical padding to make the container thinner */
        border-radius: 5px;
        margin: 10px 0;
        text-align: center; /* Center the text inside the container */
    }
    </style>
    """

    # Inject custom CSS with markdown
    st.markdown(container_style, unsafe_allow_html=True)
    st.markdown('<div class="spotify-green-container">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # Create a container with the custom class

    st.markdown(f"**Selected Playlist:** {selected_playlist}", unsafe_allow_html=True)
    st.markdown(f"**Number of songs in Playlist:** {selected_playlist_details['tracks']['total']}", unsafe_allow_html=True)


    # Make sure to safely access the "id" key
    if selected_playlist_details and "id" in selected_playlist_details:
        return selected_playlist_details["id"], selected_playlist_details['tracks']['total']
    else:
        st.sidebar.write("Error: Selected playlist details are not available.")
        return None



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
