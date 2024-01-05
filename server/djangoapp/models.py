from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    # Add any other fields you'd like

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dealer_id = models.IntegerField()  # Refers to a dealer created in Cloudant database
    TYPE_CHOICES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        # Add more choices as needed
    ]
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    year = models.DateField()

    # Add any other fields you'd like

    def __str__(self):
        return f"{self.car_make} - {self.name}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)  # Assuming 'id' is the primary key
    lat = models.FloatField()
    
    

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
from django.db import models

class DealerReview(models.Model):
    DEALERSHIP_CHOICES = [
        ('Dealer A', 'Dealer A'),
        ('Dealer B', 'Dealer B'),
        ('Dealer C', 'Dealer C'),
        # Add more choices as needed
    ]
    dealership = models.CharField(max_length=50, choices=DEALERSHIP_CHOICES)
    name = models.CharField(max_length=255)
    purchase = models.BooleanField()
    review = models.TextField()
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=50)  # You can replace this with a ForeignKey if you have a CarMake model
    car_model = models.CharField(max_length=50)  # You can replace this with a ForeignKey if you have a CarModel model
    car_year = models.IntegerField()
    
    SENTIMENT_CHOICES = [
        ('Positive', 'Positive'),
        ('Neutral', 'Neutral'),
        ('Negative', 'Negative'),
    ]
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Review for {self.dealership} - {self.name}"
