from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
from .models import ParkingSlot
from django.core.serializers import serialize
from django.views.decorators.http import require_POST

key = ""

# Create your views here.
@never_cache
def register(request):
    try:
        user = request.user
        if user.is_superuser:
            return redirect("admin")
        
        if user.is_authenticated:
            return redirect("customers:home")
 
    except Exception as e:
        pass
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already in use.")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address is already registered.")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password)
        authenticated_user = authenticate(request, username=username, password=password)
        
        auth_login(request, authenticated_user)  
        return redirect("home")
    else:
        return render(request, 'register.html', {})
    

@never_cache
def login(request):
    if request.method == "GET":
        user = request.user
        if user.is_superuser:
            return redirect("/admin")
        
        if user.is_authenticated:
            return redirect("/home")

        return render(request, 'login.html', {})

    elif request.method == "POST":
        try:
            user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        except Exception as e:
            messages.error(request, "Username is already in use.")
            return redirect("login")
        
        if user is not None:
            auth_login(request, user)  
            return redirect("/home")
        else:
            return render(request, 'login.html', {})


@login_required
@never_cache
def user_home(request):

    locations = ParkingSlot.objects.all()
    locations = serialize('json', locations)

    return render(request, 'customers/home.html', {"key": key, "locations": locations}) 


@login_required
@never_cache
def add_parking(request):
    if request.method == "POST":
        lat = request.POST.get("modal-lat-display", "")
        lng = request.POST.get("modal-lng-display", "")
        status = request.POST.get("status", "")

        if lat and lng and status:
            parking_slot = ParkingSlot()
            parking_slot.lat = float(lat)
            parking_slot.lng = float(lng)
            parking_slot.status = str(status)
            parking_slot.customer = request.user
            parking_slot.save()

    return redirect("home")

def redirection(request):
    return redirect("login")

@login_required
@never_cache
def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
@never_cache
def your_locations(request):
    locations = ParkingSlot.objects.filter(customer=request.user)
    locations = serialize('json', locations)

    return render(request, 'customers/your_locations.html', {"key": key, "locations": locations})

@login_required
@never_cache
@require_POST
def delete_location(request, id):
    try:
        location = ParkingSlot.objects.get(pk=id)
        if location.customer == request.user:
            location.delete()
        return redirect("your_locations")
    except Exception as e:
        return redirect("home")