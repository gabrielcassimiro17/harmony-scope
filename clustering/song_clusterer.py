from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


class SongClusterer:
    def __init__(self, features_cols, hyperparams):
        """
        Initializes the SongClusterer with specific features for clustering and DBSCAN hyperparameters.

        Parameters:
        - features_cols: List of columns to be used as features for clustering.
        - hyperparams: Dict containing hyperparameters for DBSCAN, specifically 'eps' and 'min_samples'.
        """
        self.features_cols = [
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "time_signature",
        ]
        self.hyperparams = hyperparams

    def apply_dbscan_clustering(self, df):
        """
        Applies DBSCAN clustering to the given DataFrame based on specified features and hyperparameters.

        Parameters:
        - df: pandas DataFrame containing the songs and their features.

        Returns:
        - Modified DataFrame with an additional 'cluster' column indicating the cluster label for each song.
        """
        # Extracting the specified features and standardizing them
        features = df[self.features_cols]
        features_standardized = StandardScaler().fit_transform(features)

        # Applying DBSCAN with the provided hyperparameters
        dbscan = DBSCAN(
            eps=self.hyperparams["eps"], min_samples=self.hyperparams["min_samples"]
        )
        clusters = dbscan.fit_predict(features_standardized)

        # Adding the cluster labels to the DataFrame
        df["cluster"] = clusters

        return df

    def analyze_clusters(self, df):
        """
        Prints out analysis of the clusters, including the number of noise points and basic statistics for each cluster.

        Parameters:
        - df: pandas DataFrame with an additional 'cluster' column from DBSCAN clustering.
        """
        noise_count = (df["cluster"] == -1).sum()
        print("Number of noise points:", noise_count)

        # Select only numeric columns for mean calculation
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        # Calculate and print mean of features for each cluster, including noise
        cluster_means = df.groupby("cluster")[numeric_cols].mean()
        print("Mean of features by cluster:")
        print(cluster_means)
