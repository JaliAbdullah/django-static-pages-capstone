# Uncomment the imports before you add the code
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "djangoapp"
urlpatterns = [
    # # path for registration
    path("register", views.registration, name="register"),
    # path for login
    path(route="login", view=views.login_user, name="login"),
    # path for logout
    path("logout", views.logout_user, name="logout"),

    # Original paths (keep for compatibility)
    path("get_dealers/", views.get_dealerships, name="get_dealers"),
    path(
        "get_dealers/<str:state>",
        views.get_dealerships,
        name="get_dealers_by_state",
    ),
    path(
        "dealer/<int:dealer_id>",
        views.get_dealer_details,
        name="dealer_details",
    ),
    path(
        "reviews/dealer/<int:dealer_id>",
        views.get_dealer_reviews,
        name="dealer_reviews",
    ),
    path(route="add_review", view=views.add_review, name="add_review"),
    path(route="get_cars", view=views.get_cars, name="getcars"),

    # NEW API ENDPOINTS (replace Node.js service)
    path("fetchDealers", views.fetch_dealers, name="fetch_dealers"),
    path("fetchDealers/<str:state>", views.fetch_dealers_by_state,
         name="fetch_dealers_by_state"),
    path("fetchDealer/<int:dealer_id>", views.fetch_dealer_by_id,
         name="fetch_dealer_by_id"),
    path("fetchReviews", views.fetch_reviews, name="fetch_reviews"),
    path("fetchReviews/dealer/<int:dealer_id>",
         views.fetch_reviews_by_dealer, name="fetch_reviews_by_dealer"),
    path("insert_review", views.insert_review, name="insert_review"),

    # Sentiment analysis endpoint
    path("analyze/<str:text>", views.analyze_sentiment_view,
         name="analyze_sentiment"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
