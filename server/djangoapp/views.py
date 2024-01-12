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
from .restapis import get_request, get_dealer_reviews_from_cf, analyze_review_sentiments, post_request



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
        url = "https://sedadak06-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Create an empty context dictionary
        context = {}

        # Add the dealerships list to the context
        context['dealerships'] = dealerships

        # Render the index.html template with the context
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...




# Define the get_dealers_from_cf function
# Define the get_dealers_from_cf function
def get_dealers_from_cf(url):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    
    try:
        # Parse the JSON response into a dictionary
        dealers_data = json.loads(json_result)
        
        # Get the row list in JSON as dealers
        dealers = dealers_data.get("rows", [])
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer.get("doc", {})
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc.get("address", ""),
                city=dealer_doc.get("city", ""),
                full_name=dealer_doc.get("full_name", ""),
                id=dealer_doc.get("id", ""),
                lat=dealer_doc.get("lat", "")
            )
            results.append(dealer_obj)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return JsonResponse({'error': 'Error decoding JSON'}, status=500)

    return results


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        # Replace 'your-cloud-function-domain/dealerships/reviews-get' with the actual URL
        url = 'https://sedadak06-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id=15'
        
        # Get reviews from the URL using the dealer_id
        reviews = get_dealer_reviews_from_cf(url, dealer_id)

        # Analyze sentiment for each review
        for review in reviews:
            review.sentiment = analyze_review_sentiments(review.review)

        # Append the list of reviews to context
        context = {
            'reviews': reviews,
            'dealer': get_object_or_404(CarDealer, id=dealer_id),
        }

        # Render a template or create an appropriate HttpResponse
        # You may need to replace 'dealer_details_template.html' with the actual template name
        return render(request, 'djangoapp/dealer_details_template.html', context)
    
def add_review(request, dealer_id):
    # Check if the request method is GET
    if request.method == 'GET':
        # Query cars with the dealer id to be reviewed
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        # Create a context dictionary with the queried cars
        context = {'cars': cars}
        # Render the add_review.html template with the context
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == "POST" and request.user.is_authenticated:
        # Get the form data from the POST request
        review_content = request.POST.get('review', '')
        purchase_status = request.POST.get('purchase', False)
        car_id = request.POST.get('car', '')
        purchase_date_str = request.POST.get('purchase_date', '')

        # Convert purchase date string to datetime format
        purchase_date = datetime.strptime(purchase_date_str, '%m/%d/%Y').isoformat()
            # Create a dictionary object called review
        review = {
            "time": datetime.utcnow().isoformat(),
            "dealership": dealer_id,
            "review": review_content,
            "purchase": purchase_status,
            "purchase_date": purchase_date,
            "car_make": CarModel.objects.get(id=car_id).make.name,
            "car_model": CarModel.objects.get(id=car_id).name,
            "car_year": CarModel.objects.get(id=car_id).year.strftime("%Y"),
            "name": request.user.username
        }

        # Create a dictionary object for the JSON payload
        json_payload = {"review": review}

            # Replace 'your-cloud-function-domain/reviews/post' with the actual URL
        url = 'https://sedadak06-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review'

            # Call the post_request method with the payload
        post_response = post_request(url, json_payload, dealerId=dealer_id)

            # Return the result of post_request
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


        # Return an error response if the request method is not POST or user is not authenticated
    return JsonResponse({'error': 'Invalid request or user not authenticated'})