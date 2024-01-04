from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'index.html')
def about_us(request):
    return render(request, 'djangoapp/about.html')
def contact_us(request):
    return render(request, 'djangoapp/contact.html')
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}!")
            return redirect('djangoapp:index')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'djangoapp/login.html', context)
@login_required
def logout_request(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('djangoapp:index')
def registration_request(request):
    context = {}
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            return redirect('djangoapp:login')
    else:
        form = UserCreationForm()
    
    context['form'] = form
    return render(request, 'djangoapp/registration.html', context)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('djangoapp:index')
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})
# Create an `about` view to render a static about page
# def about(request):
# ...


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def car_operations(request):
    # Retrieve the list of cars from the database
    cars = YourCarModel.objects.all()  # Replace YourCarModel with your actual CarModel class
    return render(request, 'djangoapp/car_operations.html', {'cars': cars})

def add_car(request):
    # Handle adding a new car (form submission) logic here
    # For example, create a new car instance and save it to the database
    return redirect('djangoapp:car_operations')  # Redirect back to the car operations page

@user_passes_test(lambda user: user.is_staff, login_url='djangoapp:login')
def car_design(request):
    # Your view logic for the car design page goes here
    return render(request, 'djangoapp/car_design.html')
