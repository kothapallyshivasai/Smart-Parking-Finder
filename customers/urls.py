from django.urls import path
from customers.views import add_parking, user_home, user_logout, your_locations, delete_location

urlpatterns = [
    path('home', user_home, name="home"),
    path('logout', user_logout, name="logout"),
    path('add_parking', add_parking, name="add_parking"),
    path('your-locations', your_locations, name="your_locations"),
    path('delete-location/<int:id>', delete_location, name="delete_location"),
]

