from langchain_core.messages import HumanMessage, SystemMessage


def analyser_prompt_template():
    return """
    You are a music expert and your job is to create an extensive analysis about a playlist.
    Focus on the genres, the popularity of the songs, the decade of the release of the songs,
    and other important information you judge is valuable. You will receive a json with the songs and
    a clustering analysis of the groups of songs.


    Songs: {songs}

    Clustering analysis: {clustering_analysis}

    """
