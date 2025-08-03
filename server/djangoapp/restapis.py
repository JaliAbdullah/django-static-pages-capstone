import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode, quote

# Load environment variables from .env file
load_dotenv()

# Load backend and sentiment analyzer URLs
backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv("sentiment_analyzer_url", default="http://localhost:5000/")

# Function to send GET request to the backend API
def get_request(endpoint, **kwargs):
    try:
        params = urlencode(kwargs) if kwargs else ""
        request_url = f"{backend_url}{endpoint}"
        if params:
            request_url += f"?{params}"

        print(f"GET from {request_url}")
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"Network exception occurred: {err}")
        return {"error": "Network exception occurred"}

# Function to call sentiment analyzer API
def analyze_review_sentiments(text):
    try:
        encoded_text = quote(text)
        request_url = f"{sentiment_analyzer_url}analyze/{encoded_text}"
        print(f"Sentiment Analysis Request: {request_url}")
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"Sentiment analysis exception: {err}")
        return {"error": "Sentiment analysis failed"}

# Function to post review data to the backend API
def post_review(data_dict):
    try:
        request_url = f"{backend_url}/insert_review"
        print(f"POST to {request_url} with data: {data_dict}")
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"Post review failed: {err}")
        return {"error": "Review submission failed"}
