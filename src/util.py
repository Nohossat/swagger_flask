import joblib
import os

from sklearn.svm import SVC


def compute_sentiment(tweets):
    default_model_path = os.path.join(os.path.dirname(__file__), "models", "grid_search_SVC.joblib")
    model = joblib.load(default_model_path)

    # infer
    preds = model.predict(tweets)
    predictions = []

    for pred in preds:
        prediction = "Positive" if pred else "Negative"
        predictions.append(prediction)

    if len(predictions) == 1:
        predictions = predictions[0]

    return predictions


if __name__ == "__main__":
    print(compute_sentiment("Je déteste"))
