import streamlit as st
from utils.spotify_utils import select_playlist_streamlit, filter_track_data, dict_to_dataframe
from clustering.song_clusterer import SongClusterer
import pandas as pd
from spotify.spotify_service import SpotifyManager
from llm.chains import build_analyser_chain
from llm.llm_config import initialize_openai_llm, initialize_google_llm

def streamlit_main(spotify_manager):
    playlist_id = select_playlist_streamlit(spotify_manager)


    if st.button("Analyze Playlist") and playlist_id:
        full_track_data = spotify_manager.get_full_track_data(playlist_id)

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

        if track_dfs:
            full_df = pd.concat(track_dfs, ignore_index=True)
            hyperparams = {'eps': 0.7, 'min_samples': 2}
            clusterer = SongClusterer(hyperparams)
            clustered_df = clusterer.apply_dbscan_clustering(full_df)
            cluster_analysis = clusterer.analyze_clusters(clustered_df)

            llm = initialize_google_llm()
            chain = build_analyser_chain(llm)

            inputs = {
                "songs": songs,
                "clustering_analysis": cluster_analysis
            }

            response = chain.invoke(inputs)

            st.write("Clustering Analysis:")
            st.dataframe(clustered_df)

            st.write("LLM Analysis Result:")
            st.write(response.content)

        else:
            st.write("No track data to save.")

if __name__ == "__main__":
    st.title("Spotify Playlist Analyzer")
    spotify_manager = SpotifyManager()
    streamlit_main(spotify_manager)
