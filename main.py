from utils.spotify_utils import choose_playlist, filter_track_data, dict_to_dataframe
from clustering.song_clusterer import SongClusterer
import pandas as pd
from spotify.spotify_service import SpotifyManager
from llm.chains import build_analyser_chain
from llm.llm_config import initialize_openai_llm, initialize_google_llm


def main():
    spotify_manager = SpotifyManager()
    playlist_id = choose_playlist(spotify_manager)
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
            print(f"Skipping track due to unexpected data format: {track_data}")

    if track_dfs:
        full_df = pd.concat(track_dfs, ignore_index=True)
        # Specify the features columns used for clustering

        # Define hyperparameters for DBSCAN
        hyperparams = {"eps": 0.7, "min_samples": 2}

        # Create an instance of SongClusterer and apply clustering
        clusterer = SongClusterer(hyperparams)
        clustered_df = clusterer.apply_dbscan_clustering(full_df)

        # Analyze the clusters
        cluster_analysis = clusterer.analyze_clusters(clustered_df)

        # Optionally, save the clustered DataFrame to a new CSV
        # clustered_df.to_csv('clustered_playlist_songs_info.csv', index=False)

        llm = initialize_google_llm()

        chain = build_analyser_chain(llm)

        inputs = {"songs": songs, "clustering_analysis": cluster_analysis}

        response = chain.invoke(inputs)

        print(response.content)

    else:
        print("No track data to save.")


if __name__ == "__main__":
    main()
