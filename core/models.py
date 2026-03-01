from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Pet(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('adoption', 'Available for Adoption'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]
    
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('giant', 'Giant'),
    ]

    name = models.CharField(max_length=100, blank=True)
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    age = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unknown')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lost')
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_pets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.breed} - {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={'pk': self.pk})

    def get_status_color(self):
        colors = {
            'lost': 'danger',
            'found': 'success',
            'adoption': 'primary',
        }
        return colors.get(self.status, 'secondary')


class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoption_requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['pet', 'requester']

    def __str__(self):
        return f"Adoption request for {self.pet.breed} by {self.requester.username}"
