import json
import os
from django.core.management.base import BaseCommand
from djangoapp.models import Dealership, Review


class Command(BaseCommand):
    help = 'Load dealership and review data from JSON files'

    def handle(self, *args, **options):
        # Path to the data files
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        dealerships_file = os.path.join(base_dir, 'database', 'data', 'dealerships.json')
        reviews_file = os.path.join(base_dir, 'database', 'data', 'reviews.json')

        # Load dealerships
        if os.path.exists(dealerships_file):
            with open(dealerships_file, 'r') as f:
                dealerships_data = json.load(f)
                
            for dealership_data in dealerships_data['dealerships']:
                dealership, created = Dealership.objects.get_or_create(
                    id=dealership_data['id'],
                    defaults={
                        'city': dealership_data.get('city', ''),
                        'state': dealership_data.get('state', ''),
                        'st': dealership_data.get('st', ''),
                        'address': dealership_data.get('address', ''),
                        'zip': dealership_data.get('zip', ''),
                        'lat': dealership_data.get('lat', 0.0),
                        'long': dealership_data.get('long', 0.0),
                        'full_name': dealership_data.get('full_name', ''),
                        'short_name': dealership_data.get('short_name', ''),
                    }
                )
                if created:
                    self.stdout.write(f"Created dealership: {dealership.short_name}")
                    
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(dealerships_data["dealerships"])} dealerships'))
        else:
            self.stdout.write(self.style.ERROR(f'Dealerships file not found: {dealerships_file}'))

        # Load reviews
        if os.path.exists(reviews_file):
            with open(reviews_file, 'r') as f:
                reviews_data = json.load(f)
                
            for review_data in reviews_data['reviews']:
                review, created = Review.objects.get_or_create(
                    id=review_data['id'],
                    defaults={
                        'name': review_data.get('name', ''),
                        'dealership': review_data.get('dealership', 0),
                        'review': review_data.get('review', ''),
                        'purchase': review_data.get('purchase', False),
                        'purchase_date': review_data.get('purchase_date', ''),
                        'car_make': review_data.get('car_make', ''),
                        'car_model': review_data.get('car_model', ''),
                        'car_year': review_data.get('car_year', 2020),
                    }
                )
                if created:
                    self.stdout.write(f"Created review: {review.name} - {review.review[:50]}...")
                    
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(reviews_data["reviews"])} reviews'))
        else:
            self.stdout.write(self.style.ERROR(f'Reviews file not found: {reviews_file}'))
