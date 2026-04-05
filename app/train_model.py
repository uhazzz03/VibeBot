import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

TRAINING_DATA_PATH = "data/mood_training_data.csv"
MODEL_PATH = "models/mood_classifier.pkl"

def train_and_save_model():
    df = pd.read_csv(TRAINING_DATA_PATH)
    x = df["text"]
    y = df["mood"]

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    model.fit(x, y)

    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)

    print(f"Model trained and data saved to {MODEL_PATH}")

if __name__ and "__main__":
    train_and_save_model()