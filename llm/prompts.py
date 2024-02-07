from langchain_core.messages import HumanMessage, SystemMessage


def analyser_prompt_template():
    return """
    As a music expert, your task is to conduct a comprehensive analysis of a given playlist, drawing insights from various musical and temporal dimensions. Your analysis should cover the following key areas:

    Genre Distribution: Examine the diversity of music genres within the playlist. Identify dominant genres and note any unique or less represented genres.
    Song Popularity: Assess the popularity of the songs. Highlight any trends observed in popularity metrics, such as the presence of mainstream hits versus niche selections.
    Decade of Release: Analyze the temporal spread of the songs' release dates. Determine if the playlist favors a particular era or spans a wide range of decades.
    Cluster Analysis: Utilize the provided clustering analysis of the song groups to explore similarities and distinctions among the songs. Discuss how songs within each cluster relate to each other in terms of genre, popularity, and era.
    In addition to these areas, consider any other significant aspects you find relevant, such as:

    Lyrical themes or mood of the songs.
    Presence of artist collaborations or features.
    Any observable pattern in song dynamics (e.g., energy, danceability).
    You will be given a JSON file containing detailed information about each song in the playlist, including genres, popularity scores, release dates, and results from a clustering analysis. Use this data to underpin your analysis with concrete examples and quantitative assessments.

    Your analysis should not only catalog the playlist's characteristics but also offer insights into its overall composition and the curator's potential intent. Provide a narrative that ties together the various data points into a cohesive understanding of the playlist's musical landscape.

    Answer in the following Language: {language}


    Songs: {songs}

    Clustering analysis: {clustering_analysis}

    """


def cluster_prompt_template():
    return """
    You are a music expert. You will receive clustering data from data in a playlist.

    Follow these steps:
    1. Create a name for each cluster based on its characteristics.
    2. Give a small description for each cluster based on its characteristics.
    3. Return a string in the format bellow:

    Format:
    ```
    Cluster 0 - Cluster name - Cluster description
    Cluster 1 - Cluster name - Cluster description
    [...]
    Cluster N - Cluster name - Cluster description
    ```

    {clusters}

    """

def recommender_prompt_template():
    return """
    Given the analysis of a playlist below, recommend 10 to 15 songs that could be added to this playlist.

    Generate general suggestions for this playlist given its characteristics as well.

    Do not suggest songs already in the playlist.

    Songs in the playlist: {songs_in_playlist}

    Playlist Analysis: {playlist_analysis}

    """
