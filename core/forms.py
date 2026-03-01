from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Pet, AdoptionRequest


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'breed', 'color', 'age', 'gender', 'size', 
            'status', 'description', 'location', 'image', 
            'contact_phone', 'contact_email'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional pet name'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Golden Retriever'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Brown'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 years'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the pet...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Area'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123-456-7890'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
        }


class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Tell us why you would be a good match for this pet...'
            })
        }


class PetSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by breed, color, location, or name...'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Pet.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('', 'All Genders')] + Pet.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    size = forms.ChoiceField(
        choices=[('', 'All Sizes')] + Pet.SIZE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Additional filter fields
    breed = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Specific breed...'
        })
    )
    color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Specific color...'
        })
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City or area...'
        })
    )
