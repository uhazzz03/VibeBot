import pandas as pd

def recommend_songs(mood):
    df = pd.read_csv("data/songs.csv")
    filtered = df[df["mood"] == mood]

    return filtered.head(5)