import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

TRAINING_DATA_PATH = "data/mood_training_data.csv"
MODEL_PATH = "models/mood_classifier.pkl"

def train_and_save_model():
    df = pd.read_csv(TRAINING_DATA_PATH)
    x = df["text"]
    y = df["mood"]

    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print("Classfication report: ")
    print(classification_report(y_test, predictions))

    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)

    print(f"Model trained and data saved to {MODEL_PATH}")

if __name__ and "__main__":
    train_and_save_model()