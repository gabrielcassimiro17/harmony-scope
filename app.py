import streamlit as st
from utils.spotify_utils import (
    select_playlist_streamlit,
    filter_track_data,
    dict_to_dataframe,
)
from utils.utils import sample_playlist, check_password
from clustering.song_clusterer import SongClusterer
import pandas as pd
from spotify.spotify_service import SpotifyManager
from llm.chains import build_analyser_chain, build_cluster_chain
from llm.llm_config import initialize_openai_llm, initialize_google_llm


def streamlit_main(spotify_manager):
    if "login_attempts" not in st.session_state:
        st.session_state["login_attempts"] = 0

    if check_password():
        # If the password is correct, display the main app
        print("Logged in")
    else:
        # If the password is incorrect, do not display the main app
        st.stop()

    current_playback = spotify_manager.get_currently_playing()
    if current_playback and current_playback.get("item"):
        item = current_playback["item"]
        st.sidebar.write("### Currently Playing")
        st.sidebar.image(item["album"]["images"][0]["url"], width=100)
        st.sidebar.write(
            f"**{item['name']}** by {''.join(artist['name'] for artist in item['artists'])}"
        )
    else:
        st.sidebar.write("### Currently Playing")
        st.sidebar.write("No track is currently playing.")

    playlist_id, number_of_tracks = select_playlist_streamlit(spotify_manager)

    language = st.sidebar.selectbox("Language:", ["English", "Portuguese"])

    if st.sidebar.button("Analyze Playlist") and playlist_id:
        # Placeholder for loading message
        loading_data_placeholder = st.empty()
        loading_data_placeholder.write("Fetching track data from Spotify...")

        big_playlist = False
        if number_of_tracks > 100:
            st.write(
                "This playlist has more than 100 songs. For the analysis, we will sample 100 songs of the playlist."
            )
            big_playlist = True

        full_track_data = spotify_manager.get_full_track_data(playlist_id)

        # Clear the loading message
        loading_data_placeholder.empty()

        # Placeholder for processing message
        processing_data_placeholder = st.empty()
        processing_data_placeholder.write("Processing track data...")

        track_dfs = []
        songs = []
        for track_data in full_track_data:
            if isinstance(track_data.get("track"), dict):
                filtered_dict = filter_track_data(track_data)
                track_df = dict_to_dataframe(filtered_dict)
                track_dfs.append(track_df)
                songs.append(filtered_dict)
            else:
                st.write(f"Skipping track due to unexpected data format: {track_data}")

        if big_playlist:
            songs = sample_playlist(songs, sample_size=100)

        for song in songs:
            song.pop("audio_features", None)

        processing_data_placeholder.empty()

        if track_dfs:
            full_df = pd.concat(track_dfs, ignore_index=True)
            hyperparams = {"eps": 0.5, "min_samples": 3}
            clusterer = SongClusterer(hyperparams)

            # Placeholder for clustering message
            clustering_data_placeholder = st.empty()
            clustering_data_placeholder.write("Applying clustering to track data...")

            clustered_df = clusterer.apply_dbscan_clustering(full_df)
            cluster_analysis = clusterer.analyze_clusters(clustered_df)
            clustering_data_placeholder.empty()

            llm = initialize_google_llm()
            cluster_chain = build_cluster_chain(llm)
            analyser_chain = build_analyser_chain(llm)

            if clustered_df["cluster"].nunique() > 1:
                ## clustering analysis call to llm
                cluster_chain_inputs = {"clusters": cluster_analysis}
                cluster_chain_response = cluster_chain.invoke(cluster_chain_inputs)
                st.subheader("Cluster Analysis")
                st.write("------------------------------------------------")
                st.write(cluster_chain_response.content)
                st.write("------------------------------------------------")

                cluster_names = cluster_chain_response.content

            else:
                cluster_names = "There are no clusters in this analysis"
                st.info(cluster_names)

            inputs = {
                "language": language,
                "songs": songs,
                "clustering_analysis": cluster_names,
            }

            # Placeholder for LLM analysis message
            llm_analysis_placeholder = st.empty()
            llm_analysis_placeholder.write("Analyzing Playlist with AI...")

            response = analyser_chain.invoke(inputs)

            llm_analysis_placeholder.empty()

            st.subheader("AI Analysis")
            st.write(response.content)

        else:
            st.write("No track data to analyze.")


if __name__ == "__main__":

    spotify_manager = SpotifyManager()
    spotify_manager.authenticate_user()

    if spotify_manager.sp:
        # Proceed with the app if the Spotify client is available
        streamlit_main(spotify_manager)
    else:
        # Optionally, handle the case where the user is not authenticated
        st.write("Please authenticate to continue.")
