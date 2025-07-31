from flask import Flask, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route("/analyze/<text>")
def analyze(text):
    scores = analyzer.polarity_scores(text)
    sentiment = "positive" if scores["compound"] >= 0.05 else "negative" if scores["compound"] <= -0.05 else "neutral"
    return jsonify({
        "text": text,
        "label": sentiment,
        "scores": scores
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
