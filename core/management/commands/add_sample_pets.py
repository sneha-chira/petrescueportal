from django.core.management.base import BaseCommand
from core.models import Pet
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Add sample pets to the database'

    def handle(self, *args, **options):
        # Get or create a default user
        user, created = User.objects.get_or_create(
            username='sample_user',
            defaults={'email': 'sample@example.com'}
        )
        
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created sample user'))

        # Sample data
        breeds = [
            'Golden Retriever', 'Labrador', 'German Shepherd', 'Bulldog', 'Poodle',
            'Beagle', 'Rottweiler', 'Yorkshire Terrier', 'Boxer', 'Siberian Husky',
            'Dachshund', 'Great Dane', 'Shih Tzu', 'Boston Terrier', 'Pomeranian',
            'Havanese', 'Shetland Sheepdog', 'Brittany', 'Cocker Spaniel', 'Australian Shepherd'
        ]
        
        colors = ['Black', 'Brown', 'White', 'Golden', 'Gray', 'Tan', 'Spotted', 'Mixed']
        locations = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte'
        ]
        
        ages = ['2 years', '3 years', '1 year', '4 years', '6 months', '5 years', '8 months', '7 years']
        genders = ['male', 'female']
        sizes = ['small', 'medium', 'large', 'giant']
        statuses = ['lost', 'found', 'adoption']
        
        descriptions = [
            'Friendly and playful, loves children and other pets. Well-trained and housebroken.',
            'Calm and gentle, perfect for families. Enjoys long walks and cuddle time.',
            'Energetic and intelligent, needs an active owner. Great for hiking and outdoor activities.',
            'Sweet and affectionate, looking for a loving home. Gets along well with everyone.',
            'Protective and loyal, excellent guard dog. Needs experienced owner.',
            'Playful and curious, loves toys and games. Perfect for active families.',
            'Gentle giant, great with kids. Needs space to roam and play.',
            'Independent but loving, enjoys both indoor and outdoor activities.',
            'Well-behaved and trained, perfect companion for seniors or quiet homes.',
            'Young and energetic, needs training and socialization. Very smart and trainable.'
        ]
        
        # Create 50 sample pets
        created_count = 0
        for i in range(50):
            pet = Pet.objects.create(
                name=f"{''.join(random.choice(['Buddy', 'Max', 'Charlie', 'Cooper', 'Rocky', 'Bear', 'Duke', 'Zeus', 'Oscar', 'Toby']).split()) if random.choice([True, False]) else ''}",
                breed=random.choice(breeds),
                color=random.choice(colors),
                age=random.choice(ages),
                gender=random.choice(genders),
                size=random.choice(sizes),
                status=random.choice(statuses),
                description=random.choice(descriptions),
                location=random.choice(locations),
                contact_phone=f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
                contact_email=f"petowner{random.randint(1, 100)}@example.com",
                reported_by=user,
                is_active=True
            )
            created_count += 1
            
            if i % 10 == 0:
                self.stdout.write(f'Created {created_count} pets...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} sample pets!'))
