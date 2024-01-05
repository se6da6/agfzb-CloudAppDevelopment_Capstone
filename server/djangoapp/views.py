from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarMake, CarModel, CarDealer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import requests
from django.http import JsonResponse


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
    if request.method == "GET":
        url = "your-cloud-function-domain/dealerships/dealer-get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(request, url)
        # Concat all dealer's full names
        dealer_names = ' '.join([dealer.full_name for dealer in dealerships])
        # Return a list of dealer full names
        return HttpResponse(dealer_names)


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

# Define the get_dealers_from_cf function
# Define the get_dealers_from_cf function
def get_dealers_from_cf(request, url):
    # Replace 'YOUR_DEALER_GET_SERVICE_URL' with the actual URL of your dealer-get service
    dealer_get_url = 'https://sedadak06-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'

    # Make the REST call to the dealer-get service
    response = requests.get(dealer_get_url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the JSON response into a list of dictionaries
        dealers_data = response.json()

        # Process the data as needed
        dealers = []

        for dealer_info in dealers_data:
            # Assuming 'full_name' is one of the keys in the dealer_info dictionary
            full_name = dealer_info.get('full_name', '')

            # Assuming other relevant keys are present in the dealer_info dictionary
            # Modify the following lines based on the actual keys in your data
            address = dealer_info.get('address', '')
            city = dealer_info.get('city', '')
            dealer_id = dealer_info.get('id', '')
            lat = dealer_info.get('lat', '')

            # Create a CarDealer object
            dealer = CarDealer(
                address=address,
                city=city,
                full_name=full_name,
                id=dealer_id,
                lat=lat,
            )

            # Add the dealer object to the list
            dealers.append(dealer)

        # Return a JsonResponse with the processed data
        return JsonResponse({'dealers': dealers})
    else:
        # Handle the error (e.g., log it or raise an exception)
        print(f"Error fetching dealers: {response.status_code}")
        return JsonResponse({'error': 'Error fetching dealers'}, status=500)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Replace 'your-cloud-function-domain/dealerships/reviews-get' with the actual URL
        url = 'https://sedadak06-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id=15'
        
        # Get reviews from the URL using the dealer_id
        reviews = get_dealer_reviews_from_cf(url, dealer_id)

        # Concatenate all review details
        review_details = ' '.join([f"Review by {review.name}: {review.review}" for review in reviews])

        # Return a list of review details
        return HttpResponse(review_details)