from django.core.management.base import BaseCommand
from core.models import AdoptionRequest, Pet, Favorite
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Add sample adoption requests and favorites'

    def handle(self, *args, **options):
        # Get users and pets
        users = list(User.objects.all())
        pets = list(Pet.objects.filter(status='adoption', is_active=True))
        
        if not users or not pets:
            self.stdout.write(self.style.ERROR('Need users and adoption pets first!'))
            return
        
        # Sample family info
        family_infos = [
            'Family with 2 kids, ages 8 and 12. Have a cat already. Large backyard.',
            'Single professional, works from home. No other pets. Apartment with balcony.',
            'Retired couple, experienced dog owners. Large house with fenced yard.',
            'Young couple, first-time pet owners. Active lifestyle, love hiking.',
            'Family with teenager, have had dogs before. Medium-sized house.',
            'Single parent with one child. Looking for a friendly companion.',
            'Couple with 3 small kids. Have experience with rescue pets.',
            'Student living with roommates. Everyone loves animals.',
            'Elderly person looking for a calm companion. Small house.',
            'Active family with 4 kids. Large farm with plenty of space.'
        ]
        
        home_types = ['house', 'apartment', 'house', 'farm', 'house', 'apartment', 'house', 'apartment', 'house', 'farm']
        experiences = ['experienced', 'first_time', 'experienced', 'first_time', 'experienced', 'multiple_pets', 'experienced', 'first_time', 'experienced', 'multiple_pets']
        
        messages = [
            'Looking for a loving companion for our family. We have experience with dogs and can provide a great home.',
            'First-time dog owner but very excited! I work from home and can give lots of attention.',
            'Experienced dog owner looking for a new best friend. Have a large, fenced yard.',
            'Want to adopt a pet to teach my kids responsibility. We\'re ready for the commitment.',
            'Looking for a hiking buddy and family pet. Very active and love outdoors.',
            'Need a friendly companion for my child. We\'re patient and loving.',
            'Want to give a rescue pet a forever home. We understand the responsibility.',
            'Looking for a pet that can join our active lifestyle. We hike and camp often.',
            'Seeking a calm companion for quiet evenings. I\'m home most of the time.',
            'Looking for a farm dog to help with chores and be part of our family.'
        ]
        
        # Create adoption requests
        created_requests = 0
        for i in range(30):
            user = random.choice(users)
            pet = random.choice(pets)
            
            # Check if request already exists
            if not AdoptionRequest.objects.filter(pet=pet, requester=user).exists():
                status = random.choice(['pending', 'pending', 'pending', 'approved', 'rejected'])
                created_date = datetime.now() - timedelta(days=random.randint(0, 90))
                
                request = AdoptionRequest.objects.create(
                    pet=pet,
                    requester=user,
                    message=random.choice(messages),
                    family_info=random.choice(family_infos),
                    home_type=random.choice(home_types),
                    pet_experience=random.choice(experiences),
                    status=status,
                    created_at=created_date
                )
                created_requests += 1
        
        # Create favorites
        created_favorites = 0
        for i in range(40):
            user = random.choice(users)
            pet = random.choice(Pet.objects.filter(is_active=True))
            
            if not Favorite.objects.filter(user=user, pet=pet).exists():
                favorite = Favorite.objects.create(
                    user=user,
                    pet=pet,
                    created_at=datetime.now() - timedelta(days=random.randint(0, 60))
                )
                created_favorites += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_requests} adoption requests and {created_favorites} favorites!'))
