from utils.spotify_utils import choose_playlist, filter_track_data, dict_to_dataframe

import pandas as pd
from spotify.spotify_service import SpotifyManager


def main():
    spotify_manager = SpotifyManager()
    playlist_id = choose_playlist(spotify_manager)
    full_track_data = spotify_manager.get_full_track_data(playlist_id)

    track_dfs = []
    for track_data in full_track_data:
        if isinstance(track_data.get('track'), dict):
            filtered_dict = filter_track_data(track_data)
            track_df = dict_to_dataframe(filtered_dict)
            track_dfs.append(track_df)
        else:
            print(f"Skipping track due to unexpected data format: {track_data}")


    # Only proceed if there are DataFrames to concatenate
    if track_dfs:
        full_df = pd.concat(track_dfs, ignore_index=True)
        full_df.to_csv('playlist_songs_info.csv', index=False)
    else:
        print("No track data to save.")


if __name__ == "__main__":
    main()
