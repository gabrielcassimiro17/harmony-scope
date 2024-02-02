# harmony-scope

Functionalities:

Playlist analyser:
Get the songs in a playlist, get the information about them, extract information
such as clusters with numerical features, and create the cluster description using an
llm, then pass the clusters and filtered track info to llm to create the analysis.

The first version will contain only one llm call, but the evolution will contain
a multi-agent conversation to create the review.


Playlist Creator:
Use the output of the playlist analyser to generate some interesting songs that
could be added to that playlist.


Song curiosities:
Get the currently listening song, use an llm agent to go into the web, search wikipedia
for the song, pass this to an LLM and return the results.
