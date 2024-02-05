from langchain_core.messages import HumanMessage, SystemMessage


def analyser_prompt_template():
    return """
    You are a music expert and your job is to create an extensive analysis about a playlist.
    Focus on the genres, the popularity of the songs, the decade of the release of the songs,
    and other important information you judge is valuable. You will receive a json with the songs and
    a clustering analysis of the groups of songs.

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
