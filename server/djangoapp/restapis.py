import requests
import json
from django.http import HttpResponse
# import related models here
from .models import CarDealer, DealerReview

from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, params=None, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    # Call get_request with a URL parameter and dealer_id
    json_result = get_request(url, dealerId=dealer_id)
    results = parse_reviews_results(json_result)
    return results

# Helper function to parse review results
def parse_reviews_results(json_result):
    results = []
    if json_result:
        reviews = json_result.get("reviews", [])
        for review in reviews:
            review_obj = DealerReview(
                dealership=review.get("dealership", ""),
                name=review.get("name", ""),
                purchase=review.get("purchase", False),
                review=review.get("review", ""),
                purchase_date=review.get("purchase_date", None),  # Make sure to convert to a proper date format
                car_make=review.get("car_make", ""),
                car_model=review.get("car_model", ""),
                car_year=review.get("car_year", 0),
            )
            
            # Assign sentiment using analyze_review_sentiments
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def get_dealer_by_id_from_cf(url, dealer_id):
    # Call get_request with a URL parameter and dealer_id
    json_result = get_request(url, dealerId=dealer_id)
    results = parse_dealer_results(json_result)
    return results

def get_dealers_by_state_from_cf(url, state):
    # Call get_request with a URL parameter and state
    json_result = get_request(url, state=state)
    results = parse_dealer_results(json_result)
    return results

# Helper function to parse dealer results
def parse_dealer_results(json_result):
    results = []
    if json_result:
        dealers = json_result.get("rows", [])
        for dealer in dealers:
            dealer_doc = dealer.get("doc", {})
            dealer_obj = CarDealer(
                address=dealer_doc.get("address", ""),
                city=dealer_doc.get("city", ""),
                full_name=dealer_doc.get("full_name", ""),
                id=dealer_doc.get("id", ""),
                lat=dealer_doc.get("lat", "")
                
                
            )
            results.append(dealer_obj)
    return results

def analyze_review_sentiments(dealerreview):
    # Replace 'your-watson-nlu-url' with the actual Watson NLU URL
    url = "https://306bcbfb-47e1-44c5-8557-e501ab2f331a-bluemix.cloudantnosqldb.appdomain.cloud",
    apikey= "fJWhxmGYw3Pmx8iSy7AMIMYodkkE9ZEfKwdLkdfOgD33"
    # Set up parameters and make the request
    params = {
        'text': text,
        'version': '2021-03-25',
        'features': 'sentiment',
        'return_analyzed_text': True,
    }
    response = get_request(url, params=params, auth=HTTPBasicAuth('apikey', api_key))
    
    # Extract sentiment from Watson NLU result
    sentiment_label = response.get('sentiment', {}).get('document', {}).get('label', 'unknown')
    
    return sentiment_label

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call post method of requests library with URL, parameters, and JSON payload
        response = requests.post(url, params=kwargs, json=json_payload,
                                 headers={'Content-Type': 'application/json'},
                                 auth=HTTPBasicAuth('apikey', api_key))
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data