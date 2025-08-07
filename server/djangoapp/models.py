from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields as needed

    def __str__(self):
        return self.name  # Return the name as the string representation


class CarModel(models.Model):
    # Many-to-one relationship to CarMake model
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    # Refers to a dealer created in Cloudant database
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)

    # Type choices
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("HATCHBACK", "Hatchback"),
        ("COUPE", "Coupe"),
        ("CONVERTIBLE", "Convertible"),
    ]
    type = models.CharField(
        max_length=20, choices=CAR_TYPES, default="SEDAN"
    )

    # Year field with validators
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)]
    )

    # Any other fields you would like to include in car model

    def __str__(self):
        # Return the car make and car model
        return f"{self.car_make.name} {self.name}"


class Dealership(models.Model):
    """Model for car dealerships"""
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=5)  # State abbreviation
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    lat = models.FloatField()
    long = models.FloatField()
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.short_name} - {self.city}, {self.st}"


class Review(models.Model):
    """Model for car reviews"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    dealership = models.IntegerField()  # Reference to dealership ID
    review = models.TextField()
    purchase = models.BooleanField()
    purchase_date = models.CharField(max_length=20)
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    car_year = models.IntegerField()
    # For sentiment analysis
    sentiment = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Review by {self.name} for dealership {self.dealership}"
