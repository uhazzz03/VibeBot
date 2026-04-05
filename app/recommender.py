import pandas as pd

def recommend_songs(mood, favorite_genres=None, favorite_moods=None):
    df = pd.read_csv("data/songs.csv")
    df["score"] = 0 #start song with zero
    df.loc[df["mood"] == mood, "score"] += 3    #Rank increase if song mood matches detected mood

    if favorite_genres:
        df.loc[df["genre"].isin(favorite_genres), "score"] += 2 #Rank increase below 3 if genre matches favorite genres

    if favorite_moods:
        df.loc[df["mood"].isin(favorite_moods), "score"] += 1   #Rank increase below 2 if mood matches favorite moods

    ranked = df[df["score"] > 0].sort_values(by="score", ascending=False)
    
    return ranked.head(5)