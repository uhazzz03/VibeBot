import pandas as pd

def recommend_songs(mood, favorite_genres=None):
    df = pd.read_csv("data/songs.csv")
    filtered = df[df["mood"] == mood]

    if favorite_genres:
        genre_filtered = filtered[filtered["genre"].isin(favorite_genres)]

        if not genre_filtered.empty:
            filtered = genre_filtered


    return filtered.head(5)