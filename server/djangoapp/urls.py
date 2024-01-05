from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('', views.get_dealerships, name='index'),
    # path for about view
    path('about/', views.about_us, name='about_us'),
    # path for contact us view
    path('contact/', views.contact_us, name='contact_us'),
    # path for registration
    path('registration/', views.registration_request, name='registration'),

    # path for login
    path('login/', views.login_request, name='login'),
    # path for logout
    path('logout/', views.logout_request, name='logout'),
    path('signup/', views.signup, name='signup'),
    path(route='', view=views.get_dealerships, name='index'),
    path('car_design/', views.car_design, name='car_design'),
    path('add_car/', views.add_car, name='add_car'),
    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)