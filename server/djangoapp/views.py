# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect

# from django.contrib import messages
# from datetime import datetime

import json
import logging
from urllib.parse import unquote

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarMake, CarModel, Dealership, Review
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review

# Import for sentiment analysis
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    import nltk
    # Download VADER lexicon if not present
    try:
        nltk.data.find('vader_lexicon')
    except LookupError:
        nltk.download('vader_lexicon')
    sentiment_analyzer = SentimentIntensityAnalyzer()
except ImportError:
    sentiment_analyzer = None

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_user(request):
    logout(request)  # Terminate user session
    data = {"userName": ""}  # Return empty username
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)

    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    username_exist = False

    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug(f"{username} is a new user")

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(
                review_detail.get("review", "")
            )
            print(f"Review: {review_detail.get('review', '')}")
            print(f"Sentiment response: {response}")
            review_detail["sentiment"] = response.get("label", "neutral")
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `add_review` view to submit a review
# def add_review(request):
@csrf_exempt
def add_review(request):
    print(
        f"add_review called - Method: {request.method}, User: {request.user}"
    )
    print(f"User is anonymous: {request.user.is_anonymous}")

    if request.method != "POST":
        return JsonResponse(
            {"status": 400, "message": "Only POST method allowed"}
        )

    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            print(f"Review data received: {data}")
            response = post_review(data)
            print(f"Backend response: {response}")
            return JsonResponse({"status": 200})
        except Exception as e:
            print(f"Error in posting review: {str(e)}")
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )
    else:
        print("User is not authenticated")
        return JsonResponse({"status": 403, "message": "Unauthorized"})


# Create a get_cars view to get list of cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related("car_make")
    cars = []
    for car_model in car_models:
        cars.append(
            {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        )
    return JsonResponse({"CarModels": cars})


# ============================================================================
# NEW API ENDPOINTS TO REPLACE NODE.JS SERVICE
# ============================================================================

@csrf_exempt
def fetch_dealers(request):
    """Fetch all dealerships"""
    try:
        dealerships = Dealership.objects.all()
        dealers_list = []
        for dealer in dealerships:
            dealers_list.append({
                'id': dealer.id,
                'city': dealer.city,
                'state': dealer.state,
                'st': dealer.st,
                'address': dealer.address,
                'zip': dealer.zip,
                'lat': dealer.lat,
                'long': dealer.long,
                'full_name': dealer.full_name,
                'short_name': dealer.short_name,
            })
        return JsonResponse(dealers_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def fetch_dealers_by_state(request, state):
    """Fetch dealerships by state"""
    try:
        dealerships = Dealership.objects.filter(state=state)
        dealers_list = []
        for dealer in dealerships:
            dealers_list.append({
                'id': dealer.id,
                'city': dealer.city,
                'state': dealer.state,
                'st': dealer.st,
                'address': dealer.address,
                'zip': dealer.zip,
                'lat': dealer.lat,
                'long': dealer.long,
                'full_name': dealer.full_name,
                'short_name': dealer.short_name,
            })
        return JsonResponse(dealers_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def fetch_dealer_by_id(request, dealer_id):
    """Fetch a specific dealer by ID"""
    try:
        dealer = Dealership.objects.get(id=dealer_id)
        dealer_data = {
            'id': dealer.id,
            'city': dealer.city,
            'state': dealer.state,
            'st': dealer.st,
            'address': dealer.address,
            'zip': dealer.zip,
            'lat': dealer.lat,
            'long': dealer.long,
            'full_name': dealer.full_name,
            'short_name': dealer.short_name,
        }
        return JsonResponse(dealer_data)
    except Dealership.DoesNotExist:
        return JsonResponse({'message': 'Dealer not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def fetch_reviews(request):
    """Fetch all reviews"""
    try:
        reviews = Review.objects.all()
        reviews_list = []
        for review in reviews:
            reviews_list.append({
                'id': review.id,
                'name': review.name,
                'dealership': review.dealership,
                'review': review.review,
                'purchase': review.purchase,
                'purchase_date': review.purchase_date,
                'car_make': review.car_make,
                'car_model': review.car_model,
                'car_year': review.car_year,
                'sentiment': review.sentiment,
            })
        return JsonResponse(reviews_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def fetch_reviews_by_dealer(request, dealer_id):
    """Fetch reviews for a specific dealer"""
    try:
        reviews = Review.objects.filter(dealership=dealer_id)
        reviews_list = []
        for review in reviews:
            # Analyze sentiment if not already done
            sentiment = review.sentiment
            if not sentiment and sentiment_analyzer:
                sentiment = analyze_sentiment_local(review.review)
                review.sentiment = sentiment
                review.save()
            
            reviews_list.append({
                'id': review.id,
                'name': review.name,
                'dealership': review.dealership,
                'review': review.review,
                'purchase': review.purchase,
                'purchase_date': review.purchase_date,
                'car_make': review.car_make,
                'car_model': review.car_model,
                'car_year': review.car_year,
                'sentiment': sentiment,
            })
        return JsonResponse(reviews_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def insert_review(request):
    """Insert a new review"""
    try:
        data = json.loads(request.body)
        
        # Get the next available ID
        last_review = Review.objects.order_by('-id').first()
        new_id = (last_review.id + 1) if last_review else 1
        
        # Analyze sentiment
        sentiment = None
        if sentiment_analyzer and data.get('review'):
            sentiment = analyze_sentiment_local(data['review'])
        
        review = Review.objects.create(
            id=new_id,
            name=data.get('name', ''),
            dealership=data.get('dealership', 0),
            review=data.get('review', ''),
            purchase=data.get('purchase', False),
            purchase_date=data.get('purchase_date', ''),
            car_make=data.get('car_make', ''),
            car_model=data.get('car_model', ''),
            car_year=data.get('car_year', 2020),
            sentiment=sentiment,
        )
        
        return JsonResponse({
            'id': review.id,
            'name': review.name,
            'dealership': review.dealership,
            'review': review.review,
            'purchase': review.purchase,
            'purchase_date': review.purchase_date,
            'car_make': review.car_make,
            'car_model': review.car_model,
            'car_year': review.car_year,
            'sentiment': review.sentiment,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def analyze_sentiment_view(request, text):
    """Analyze sentiment of given text"""
    try:
        # URL decode the text
        decoded_text = unquote(text)
        sentiment = analyze_sentiment_local(decoded_text)
        
        return JsonResponse({
            'text': decoded_text,
            'sentiment': sentiment,
            'label': sentiment  # For compatibility with existing frontend
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def analyze_sentiment_local(text):
    """Local sentiment analysis function"""
    if not sentiment_analyzer:
        return "neutral"
    
    try:
        scores = sentiment_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return "neutral"
