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
