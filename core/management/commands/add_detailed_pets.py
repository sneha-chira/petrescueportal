from django.core.management.base import BaseCommand
from core.models import Pet
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Add more diverse sample pets with detailed information'

    def handle(self, *args, **options):
        # Get or create a default user
        user, created = User.objects.get_or_create(
            username='detailed_user',
            defaults={'email': 'detailed@example.com'}
        )
        
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created detailed user'))

        # More diverse and realistic pet data
        detailed_pets = [
            {
                'name': 'Bella',
                'breed': 'Golden Retriever',
                'color': 'Golden',
                'age': '3 years',
                'gender': 'female',
                'size': 'large',
                'status': 'adoption',
                'description': 'Beautiful Golden Retriever with a gentle temperament. Great with kids and other pets. Fully vaccinated and house-trained. Loves playing fetch and swimming.',
                'location': 'San Francisco, CA',
                'contact_phone': '+1-415-555-0123',
                'contact_email': 'bella.adopter@email.com'
            },
            {
                'name': 'Max',
                'breed': 'German Shepherd',
                'color': 'Black and Tan',
                'age': '2 years',
                'gender': 'male',
                'size': 'large',
                'status': 'lost',
                'description': 'Friendly German Shepherd, very loyal and protective. Knows basic commands. Last seen wearing a red collar. Very missed by family.',
                'location': 'Austin, TX',
                'contact_phone': '+1-512-555-0456',
                'contact_email': 'max.owner@email.com'
            },
            {
                'name': 'Luna',
                'breed': 'Siamese Cat',
                'color': 'Cream and Brown',
                'age': '1 year',
                'gender': 'female',
                'size': 'small',
                'status': 'found',
                'description': 'Beautiful Siamese cat found near the park. Very friendly and appears well-cared for. Has striking blue eyes. Not microchipped.',
                'location': 'Seattle, WA',
                'contact_phone': '+1-206-555-0789',
                'contact_email': 'luna.finder@email.com'
            },
            {
                'name': 'Charlie',
                'breed': 'Beagle',
                'color': 'Tricolor',
                'age': '4 years',
                'gender': 'male',
                'size': 'medium',
                'status': 'adoption',
                'description': 'Playful Beagle with lots of energy. Great for active families. Loves children and gets along with other dogs. Fully vetted.',
                'location': 'Denver, CO',
                'contact_phone': '+1-303-555-0234',
                'contact_email': 'charlie.adopt@email.com'
            },
            {
                'name': 'Daisy',
                'breed': 'Persian Cat',
                'color': 'White',
                'age': '2 years',
                'gender': 'female',
                'size': 'small',
                'status': 'lost',
                'description': 'Fluffy white Persian cat with beautiful blue eyes. Very gentle and shy. Last seen in backyard. Has distinctive pink collar.',
                'location': 'Portland, OR',
                'contact_phone': '+1-503-555-0567',
                'contact_email': 'daisy.family@email.com'
            },
            {
                'name': 'Rocky',
                'breed': 'Bulldog',
                'color': 'Brindle',
                'age': '5 years',
                'gender': 'male',
                'size': 'medium',
                'status': 'adoption',
                'description': 'Calm and affectionate Bulldog. Perfect apartment companion. Low energy, loves cuddling. Great with seniors.',
                'location': 'Chicago, IL',
                'contact_phone': '+1-312-555-0890',
                'contact_email': 'rocky.rescue@email.com'
            },
            {
                'name': 'Mittens',
                'breed': 'Tabby Cat',
                'color': 'Orange and White',
                'age': '6 months',
                'gender': 'male',
                'size': 'small',
                'status': 'found',
                'description': 'Adorable orange tabby kitten found near shopping center. Very playful and healthy. Appears to be about 6 months old.',
                'location': 'Boston, MA',
                'contact_phone': '+1-617-555-0123',
                'contact_email': 'mittens.found@email.com'
            },
            {
                'name': 'Sadie',
                'breed': 'Labrador Retriever',
                'color': 'Chocolate',
                'age': '1 year',
                'gender': 'female',
                'size': 'large',
                'status': 'lost',
                'description': 'Energetic chocolate Lab, very friendly. Loves water and playing fetch. Last seen at the dog park. Family is devastated.',
                'location': 'Miami, FL',
                'contact_phone': '+1-305-555-0345',
                'contact_email': 'sadie.owner@email.com'
            },
            {
                'name': 'Oliver',
                'breed': 'Maine Coon',
                'color': 'Gray',
                'age': '3 years',
                'gender': 'male',
                'size': 'large',
                'status': 'adoption',
                'description': 'Majestic Maine Coon with beautiful long fur. Gentle giant, very calm and loving. Great with children.',
                'location': 'Phoenix, AZ',
                'contact_phone': '+1-602-555-0678',
                'contact_email': 'oliver.adopt@email.com'
            },
            {
                'name': 'Whiskers',
                'breed': 'Domestic Shorthair',
                'color': 'Black',
                'age': '2 years',
                'gender': 'male',
                'size': 'small',
                'status': 'found',
                'description': 'Sleek black cat found near apartment complex. Very friendly and appears to be well-fed. Has green eyes.',
                'location': 'Las Vegas, NV',
                'contact_phone': '+1-702-555-0901',
                'contact_email': 'whiskers.finder@email.com'
            },
            {
                'name': 'Lucy',
                'breed': 'Poodle',
                'color': 'White',
                'age': '4 years',
                'gender': 'female',
                'size': 'medium',
                'status': 'adoption',
                'description': 'Elegant white Poodle, hypoallergenic coat. Very intelligent and well-trained. Perfect for families with allergies.',
                'location': 'Nashville, TN',
                'contact_phone': '+1-615-555-0234',
                'contact_email': 'lucy.poodle@email.com'
            },
            {
                'name': 'Duke',
                'breed': 'Boxer',
                'color': 'Fawn',
                'age': '3 years',
                'gender': 'male',
                'size': 'large',
                'status': 'lost',
                'description': 'Strong Boxer with lots of energy. Great with kids and protective of family. Last seen wearing blue collar.',
                'location': 'Philadelphia, PA',
                'contact_phone': '+1-215-555-0567',
                'contact_email': 'duke.family@email.com'
            },
            {
                'name': 'Sophie',
                'breed': 'Ragdoll Cat',
                'color': 'Seal Point',
                'age': '2 years',
                'gender': 'female',
                'size': 'medium',
                'status': 'found',
                'description': 'Beautiful Ragdoll cat with striking blue eyes. Very affectionate and calm. Found near residential area.',
                'location': 'San Diego, CA',
                'contact_phone': '+1-619-555-0789',
                'contact_email': 'sophie.found@email.com'
            },
            {
                'name': 'Cooper',
                'breed': 'Australian Shepherd',
                'color': 'Blue Merle',
                'age': '2 years',
                'gender': 'male',
                'size': 'medium',
                'status': 'adoption',
                'description': 'Intelligent Australian Shepherd with beautiful blue merle coat. High energy, needs active family. Great at agility.',
                'location': 'Atlanta, GA',
                'contact_phone': '+1-404-555-0901',
                'contact_email': 'cooper.adopt@email.com'
            },
            {
                'name': 'Shadow',
                'breed': 'Black Cat',
                'color': 'Black',
                'age': '1 year',
                'gender': 'male',
                'size': 'small',
                'status': 'lost',
                'description': 'Sleek black cat, very shy but friendly. Has distinctive white patch on chest. Much loved family member.',
                'location': 'Dallas, TX',
                'contact_phone': '+1-214-555-0123',
                'contact_email': 'shadow.owner@email.com'
            },
            {
                'name': 'Bella',
                'breed': 'Husky',
                'color': 'Black and White',
                'age': '3 years',
                'gender': 'female',
                'size': 'large',
                'status': 'adoption',
                'description': 'Stunning Husky with striking blue eyes. Very energetic and needs lots of exercise. Great for cold climates.',
                'location': 'Minneapolis, MN',
                'contact_phone': '+1-612-555-0345',
                'contact_email': 'bella.husky@email.com'
            },
            {
                'name': 'Milo',
                'breed': 'Tabby Cat',
                'color': 'Gray and White',
                'age': '8 months',
                'gender': 'male',
                'size': 'small',
                'status': 'found',
                'description': 'Cute gray and white tabby kitten found in garden. Very playful and healthy. Loves attention.',
                'location': 'Charlotte, NC',
                'contact_phone': '+1-704-555-0567',
                'contact_email': 'milo.kitten@email.com'
            },
            {
                'name': 'Bear',
                'breed': 'Saint Bernard',
                'color': 'White and Brown',
                'age': '4 years',
                'gender': 'male',
                'size': 'giant',
                'status': 'adoption',
                'description': 'Gentle giant Saint Bernard. Very calm and great with children. Needs space due to size. Perfect family dog.',
                'location': 'Salt Lake City, UT',
                'contact_phone': '+1-801-555-0789',
                'contact_email': 'bear.saint@email.com'
            }
        ]

        # Create detailed pets
        created_count = 0
        for pet_data in detailed_pets:
            pet = Pet.objects.create(
                name=pet_data['name'],
                breed=pet_data['breed'],
                color=pet_data['color'],
                age=pet_data['age'],
                gender=pet_data['gender'],
                size=pet_data['size'],
                status=pet_data['status'],
                description=pet_data['description'],
                location=pet_data['location'],
                contact_phone=pet_data['contact_phone'],
                contact_email=pet_data['contact_email'],
                reported_by=user,
                is_active=True
            )
            created_count += 1
            
            if created_count % 5 == 0:
                self.stdout.write(f'Created {created_count} detailed pets...')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} detailed sample pets!'))
