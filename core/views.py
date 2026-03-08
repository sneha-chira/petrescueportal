from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Pet, AdoptionRequest, Favorite
from .forms import PetForm, AdoptionRequestForm, PetSearchForm, CustomUserCreationForm
from django.contrib.auth import login

# --- VIEWS ---
def home(request):
    latest_pets = Pet.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'latest_pets': latest_pets})

def login_view(request):
    from django.contrib.auth import authenticate, login
    from django.contrib.auth.forms import AuthenticationForm
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')

def report_lost_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            if request.user.is_authenticated:
                pet.reported_by = request.user
            else:
                # Create a default user or handle anonymous submission
                from django.contrib.auth.models import User
                default_user, created = User.objects.get_or_create(username='anonymous')
                pet.reported_by = default_user
            pet.status = 'lost'
            pet.save()
            messages.success(request, 'Lost pet reported successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetForm(initial={'status': 'lost'})
    return render(request, 'lost_pet_form.html', {'form': form})

def report_found_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            if request.user.is_authenticated:
                pet.reported_by = request.user
            else:
                # Create a default user or handle anonymous submission
                from django.contrib.auth.models import User
                default_user, created = User.objects.get_or_create(username='anonymous')
                pet.reported_by = default_user
            pet.status = 'found'
            pet.save()
            messages.success(request, 'Found pet reported successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetForm(initial={'status': 'found'})
    return render(request, 'found_pet_form.html', {'form': form})

@login_required
def adoption_form(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.reported_by = request.user
            pet.status = 'adoption'
            pet.save()
            messages.success(request, 'Pet listed for adoption successfully!')
            return redirect('pet_detail', pk=pet.pk)
    else:
        form = PetForm(initial={'status': 'adoption'})
    return render(request, 'adoption_form.html', {'form': form})

def lost_pets_list(request):
    form = PetSearchForm(request.GET)
    pets = Pet.objects.filter(is_active=True, status='lost')
    
    # Check favorites for authenticated users
    if request.user.is_authenticated:
        favorite_pet_ids = Favorite.objects.filter(user=request.user).values_list('pet_id', flat=True)
        for pet in pets:
            pet.is_favorite = pet.id in favorite_pet_ids
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        gender = form.cleaned_data.get('gender')
        size = form.cleaned_data.get('size')
        breed = form.cleaned_data.get('breed')
        color = form.cleaned_data.get('color')
        location = form.cleaned_data.get('location')
        
        if search:
            pets = pets.filter(
                Q(breed__icontains=search) |
                Q(color__icontains=search) |
                Q(location__icontains=search) |
                Q(name__icontains=search)
            )
        if gender:
            pets = pets.filter(gender=gender)
        if size:
            pets = pets.filter(size=size)
        if breed:
            pets = pets.filter(breed__icontains=breed)
        if color:
            pets = pets.filter(color__icontains=color)
        if location:
            pets = pets.filter(location__icontains=location)
    
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pet_list.html', {
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': True,
        'form': form,
        'title': 'Lost Pets'
    })

def found_pets_list(request):
    form = PetSearchForm(request.GET)
    pets = Pet.objects.filter(is_active=True, status='found')
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        gender = form.cleaned_data.get('gender')
        size = form.cleaned_data.get('size')
        breed = form.cleaned_data.get('breed')
        color = form.cleaned_data.get('color')
        location = form.cleaned_data.get('location')
        
        if search:
            pets = pets.filter(
                Q(breed__icontains=search) |
                Q(color__icontains=search) |
                Q(location__icontains=search) |
                Q(name__icontains=search)
            )
        if gender:
            pets = pets.filter(gender=gender)
        if size:
            pets = pets.filter(size=size)
        if breed:
            pets = pets.filter(breed__icontains=breed)
        if color:
            pets = pets.filter(color__icontains=color)
        if location:
            pets = pets.filter(location__icontains=location)
    
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pet_list.html', {
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': True,
        'form': form,
        'title': 'Found Pets'
    })

def adoption_list(request):
    form = PetSearchForm(request.GET)
    pets = Pet.objects.filter(is_active=True, status='adoption')
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        status = form.cleaned_data.get('status')
        gender = form.cleaned_data.get('gender')
        size = form.cleaned_data.get('size')
        
        if search:
            pets = pets.filter(
                Q(breed__icontains=search) |
                Q(color__icontains=search) |
                Q(location__icontains=search) |
                Q(name__icontains=search)
            )
        if status:
            pets = pets.filter(status=status)
        if gender:
            pets = pets.filter(gender=gender)
        if size:
            pets = pets.filter(size=size)
    
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'pet_list.html', {
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': True,
        'form': form,
        'title': 'Pets Available for Adoption'
    })

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk, is_active=True)
    adoption_request_form = None
    is_favorite = False
    
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, pet=pet).exists()
    
    if request.user.is_authenticated and pet.status == 'adoption':
        if request.method == 'POST':
            adoption_request_form = AdoptionRequestForm(request.POST)
            if adoption_request_form.is_valid():
                adoption_request = adoption_request_form.save(commit=False)
                adoption_request.pet = pet
                adoption_request.requester = request.user
                adoption_request.save()
                messages.success(request, 'Your adoption request has been submitted!')
                return redirect('pet_detail', pk=pet.pk)
        else:
            adoption_request_form = AdoptionRequestForm()
    
    return render(request, 'pet_detail.html', {
        'object': pet,
        'adoption_request_form': adoption_request_form,
        'is_favorite': is_favorite
    })

@login_required
def dashboard(request):
    user_pets = Pet.objects.filter(reported_by=request.user, is_active=True)
    adoption_requests = AdoptionRequest.objects.filter(requester=request.user)
    
    return render(request, 'dashboard.html', {
        'user_pets': user_pets,
        'adoption_requests': adoption_requests
    })

@login_required
def submit_adoption_request(request, pk):
    pet = get_object_or_404(Pet, pk=pk, is_active=True, status='adoption')
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        
        # Check if user already submitted a request for this pet
        existing_request = AdoptionRequest.objects.filter(pet=pet, requester=request.user).first()
        if existing_request:
            messages.warning(request, 'You have already submitted an adoption request for this pet.')
            return redirect('pet_detail', pk=pet.pk)
        
        # Create new adoption request
        adoption_request = AdoptionRequest.objects.create(
            pet=pet,
            requester=request.user,
            message=message,
            status='pending'
        )
        
        messages.success(request, 'Your adoption request has been submitted successfully! The admin will review it soon.')
        return redirect('pet_detail', pk=pet.pk)
    
    return redirect('pet_detail', pk=pet.pk)

@login_required
def admin_adoption_requests(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    requests = AdoptionRequest.objects.all().order_by('-created_at')
    
    return render(request, 'admin/adoption_requests.html', {
        'adoption_requests': requests
    })

@login_required
def approve_adoption_request(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    adoption_request = get_object_or_404(AdoptionRequest, pk=pk)
    adoption_request.status = 'approved'
    adoption_request.save()
    
    # Update pet status to show it's adopted
    pet = adoption_request.pet
    pet.is_active = False
    pet.save()
    
    # Create notification message (you can implement a proper notification system later)
    messages.success(request, f'Adoption request for {pet.name or pet.breed} has been approved!')
    
    return redirect('admin_adoption_requests')

@login_required
def reject_adoption_request(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    adoption_request = get_object_or_404(AdoptionRequest, pk=pk)
    adoption_request.status = 'rejected'
    adoption_request.save()
    
    messages.success(request, f'Adoption request for {adoption_request.pet.name or adoption_request.pet.breed} has been rejected.')
    
    return redirect('admin_adoption_requests')

@login_required
def analytics_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    from django.db.models import Count, Q, Avg
    from datetime import datetime, timedelta
    import calendar
    
    # Get date ranges
    today = datetime.now()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    last_90_days = today - timedelta(days=90)
    
    # Pet Statistics
    total_pets = Pet.objects.count()
    active_pets = Pet.objects.filter(is_active=True).count()
    lost_pets = Pet.objects.filter(status='lost').count()
    found_pets = Pet.objects.filter(status='found').count()
    adoption_pets = Pet.objects.filter(status='adoption').count()
    
    # Recent pets (last 30 days)
    recent_pets = Pet.objects.filter(created_at__gte=last_30_days).count()
    
    # Adoption Request Statistics
    total_requests = AdoptionRequest.objects.count()
    pending_requests = AdoptionRequest.objects.filter(status='pending').count()
    approved_requests = AdoptionRequest.objects.filter(status='approved').count()
    rejected_requests = AdoptionRequest.objects.filter(status='rejected').count()
    
    # Recent requests (last 7 days)
    recent_requests = AdoptionRequest.objects.filter(created_at__gte=last_7_days).count()
    
    # Monthly trends (last 6 months)
    monthly_pets = []
    monthly_requests = []
    for i in range(6):
        month_start = today.replace(day=1) - timedelta(days=i*30)
        month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
        
        pets_in_month = Pet.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).count()
        
        requests_in_month = AdoptionRequest.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end
        ).count()
        
        monthly_pets.append({
            'month': month_start.strftime('%b'),
            'count': pets_in_month
        })
        monthly_requests.append({
            'month': month_start.strftime('%b'),
            'count': requests_in_month
        })
    
    monthly_pets.reverse()
    monthly_requests.reverse()
    
    # Top locations with counts
    top_locations = Pet.objects.values('location').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Top breeds with counts
    top_breeds = Pet.objects.values('breed').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Pet status distribution
    status_distribution = [
        {'status': 'Lost', 'count': lost_pets, 'color': '#dc3545'},
        {'status': 'Found', 'count': found_pets, 'color': '#198754'},
        {'status': 'Available for Adoption', 'count': adoption_pets, 'color': '#0d6efd'}
    ]
    
    # Request status distribution
    request_distribution = [
        {'status': 'Pending', 'count': pending_requests, 'color': '#ffc107'},
        {'status': 'Approved', 'count': approved_requests, 'color': '#198754'},
        {'status': 'Rejected', 'count': rejected_requests, 'color': '#dc3545'}
    ]
    
    # Home type distribution
    home_type_stats = AdoptionRequest.objects.values('home_type').annotate(
        count=Count('id')
    ).exclude(home_type__isnull=True)
    
    # Experience level distribution
    experience_stats = AdoptionRequest.objects.values('pet_experience').annotate(
        count=Count('id')
    ).exclude(pet_experience__isnull=True)
    
    # Recent activity
    recent_adoption_requests = AdoptionRequest.objects.select_related(
        'pet', 'requester'
    ).order_by('-created_at')[:10]
    
    # Performance metrics
    approval_rate = (approved_requests / total_requests * 100) if total_requests > 0 else 0
    average_requests_per_day = total_requests / 90 if total_requests > 0 else 0
    pets_with_images = Pet.objects.exclude(image='').count()
    image_upload_rate = (pets_with_images / total_pets * 100) if total_pets > 0 else 0
    
    context = {
        # Basic stats
        'total_pets': total_pets,
        'active_pets': active_pets,
        'lost_pets': lost_pets,
        'found_pets': found_pets,
        'adoption_pets': adoption_pets,
        'recent_pets': recent_pets,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'recent_requests': recent_requests,
        
        # Charts data
        'monthly_pets': monthly_pets,
        'monthly_requests': monthly_requests,
        'status_distribution': status_distribution,
        'request_distribution': request_distribution,
        'home_type_stats': home_type_stats,
        'experience_stats': experience_stats,
        
        # Top data
        'top_locations': top_locations,
        'top_breeds': top_breeds,
        'recent_adoption_requests': recent_adoption_requests,
        
        # Performance metrics
        'approval_rate': round(approval_rate, 1),
        'average_requests_per_day': round(average_requests_per_day, 1),
        'image_upload_rate': round(image_upload_rate, 1),
    }
    
    return render(request, 'admin/analytics_dashboard.html', context)

@login_required
def toggle_favorite(request, pk):
    pet = get_object_or_404(Pet, pk=pk, is_active=True)
    favorite, created = Favorite.objects.get_or_create(user=request.user, pet=pet)
    
    if not created:
        # If favorite already exists, remove it
        favorite.delete()
        messages.success(request, f'{pet.name or pet.breed} removed from favorites')
    else:
        messages.success(request, f'{pet.name or pet.breed} added to favorites')
    
    return redirect('pet_detail', pk=pk)

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('pet')
    return render(request, 'favorites.html', {'favorites': favorites})
