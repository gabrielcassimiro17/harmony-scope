import streamlit as st
from utils.spotify_utils import select_playlist_streamlit, filter_track_data, dict_to_dataframe
from clustering.song_clusterer import SongClusterer
import pandas as pd
from spotify.spotify_service import SpotifyManager
from llm.chains import build_analyser_chain
from llm.llm_config import initialize_openai_llm, initialize_google_llm

def streamlit_main(spotify_manager):
    # Modified to use the select_playlist_streamlit function directly in the UI
    playlist_id = select_playlist_streamlit(spotify_manager)

    current_playback = spotify_manager.get_currently_playing()
    if current_playback and current_playback.get('item'):
        item = current_playback['item']
        st.sidebar.write("### Currently Playing")
        st.sidebar.image(item['album']['images'][0]['url'], width=100)
        st.sidebar.write(f"**{item['name']}** by {''.join(artist['name'] for artist in item['artists'])}")
    else:
        st.sidebar.write("### Currently Playing")
        st.sidebar.write("No track is currently playing.")

    if st.sidebar.button("Analyze Playlist") and playlist_id:
        # Placeholder for loading message
        loading_data_placeholder = st.empty()
        loading_data_placeholder.write("Fetching track data from Spotify...")

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

        processing_data_placeholder.empty()

        if track_dfs:
            full_df = pd.concat(track_dfs, ignore_index=True)
            hyperparams = {'eps': 0.7, 'min_samples': 2}
            clusterer = SongClusterer(hyperparams)

            # Placeholder for clustering message
            clustering_data_placeholder = st.empty()
            clustering_data_placeholder.write("Applying clustering to track data...")

            clustered_df = clusterer.apply_dbscan_clustering(full_df)
            cluster_analysis = clusterer.analyze_clusters(clustered_df)
            clustering_data_placeholder.empty()

            llm = initialize_google_llm()
            chain = build_analyser_chain(llm)

            inputs = {
                "songs": songs,
                "clustering_analysis": cluster_analysis
            }

            # Placeholder for LLM analysis message
            llm_analysis_placeholder = st.empty()
            llm_analysis_placeholder.write("Analyzing Playlist with AI...")

            response = chain.invoke(inputs)

            llm_analysis_placeholder.empty()

            st.write("LLM Analysis Result:")
            st.write(response.content)

        else:
            st.write("No track data to analyze.")

if __name__ == "__main__":
    st.title("Spotify Playlist Analyzer")
    spotify_manager = SpotifyManager()
    streamlit_main(spotify_manager)
