#!/usr/bin/env python3
import requests


# Test the sentiment analyzer directly
def test_sentiment_analyzer():
    url = (
        "http://localhost:5000/analyze/"
        "This%20car%20is%20absolutely%20amazing%20and%20fantastic"
    )
    response = requests.get(url)
    print("Sentiment analyzer response:", response.json())


# Test Django sentiment analysis
def test_django_sentiment():
    url = "http://localhost:8000/djangoapp/reviews/dealer/15"
    response = requests.get(url)
    data = response.json()
    print("Django reviews response:")
    for review in data.get("reviews", []):
        print(f"Review: {review.get('review', '')[:50]}...")
        print(f"Sentiment: {review.get('sentiment', 'unknown')}")
        print("---")


if __name__ == "__main__":
    print("Testing sentiment analyzer...")
    test_sentiment_analyzer()
    print("\nTesting Django reviews...")
    test_django_sentiment()
