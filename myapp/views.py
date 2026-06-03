from . models import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import PermissionDenied

import os 
import joblib
import pandas as pd
path = os.path.dirname(__file__)
model = joblib.load(open(os.path.join(path, "house_price_model.pkl"),"rb"))

# Create your views here.

def home(req):
    tab = 'home'
    return render(req, 'home.html', {'tab':tab})

@login_required(login_url='login')
def prediction(req):
    tab = 'prediction'

    if req.method == 'POST':
        medinc = req.POST['medinc']
        houseage = req.POST['houseage']
        averooms = req.POST['averooms']
        avebedrms = req.POST['avebedrms']
        population = req.POST['population']
        aveoccup = req.POST['aveoccup']
        latitude = req.POST['latitude']
        longitude = req.POST['longitude']
        res = model.predict([[medinc, houseage, averooms, avebedrms, population, aveoccup, latitude, longitude]])[0].round(2)
        res = res*100000
        hpp = Price_Prediction( user = req.user, medinc = medinc, houseage = houseage, averooms = averooms, avebedrms = avebedrms, population = population, aveoccup = aveoccup, latitude = latitude, longitude = longitude, res = res)
        hpp.save()
    else:
        res = 0
    return render(req, 'prediction.html', {'res':res, 'tab':tab})


def about(req):
    tab = 'about'
    return render(req, 'about.html', {'tab':tab})

@login_required(login_url='login')
def history(req):
    tab = 'history'
    his = Price_Prediction.objects.filter(user = req.user)
    return render(req, 'history.html', {'tab':tab, 'his':his})

def user_login(req):
    tab = 'login'

    if req.method == 'POST':
        email    = req.POST['email']
        password = req.POST['password']

        #  Step 1 — email se username dhundo
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username  # username = email hai humara
        except User.DoesNotExist:
            messages.error(req, 'Wrong Email!')
            return render(req, 'login.html', {'tab': tab})

        #  Step 2 — username aur password check karo
        user = authenticate(req, username=username, password=password)

        #  Step 3 — agar sahi hai to login karo
        if user is not None:
            auth_login(req, user)
            # messages.success(req, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(req, 'Wrong Password!')
            return render(req, 'login.html', {'tab': tab})

    return render(req, 'login.html', {'tab': tab})

def register(req):
    tab = 'register'
    if req.method == 'POST':
        first_name = req.POST['first_name']
        last_name  = req.POST['last_name']
        phone      = req.POST['phone']
        email      = req.POST['email']    # sirf email form se liya
        password   = req.POST['password1']

        #  Email check
        if User.objects.filter(email=email).exists():
            messages.error(req, 'Email already registered!')
            return render(req, 'register.html', {'tab': tab})

        #  Phone check
        if UserProfile.objects.filter(phone=phone).exists():
            messages.error(req, ' phone already registered!')
            return render(req, 'register.html', {'tab': tab})

        #  Code mein dono jagah same email save karo
        user = User.objects.create_user(
            username = email,   
            email    = email, 
            first_name = first_name,
            last_name  = last_name,
            password   = password
        )

        UserProfile.objects.create(
            user  = user,
            phone = phone
        )
        req.session['is_registered'] = True

        # messages.success(req, 'Registration successful!')
        return redirect('login')

    return render(req, 'register.html', {'tab': tab})

@login_required(login_url='login')
def dashboard(req):
    tab = 'dashboard'
    
    # User ki profile lo
    user_profile = UserProfile.objects.get(user=req.user)
    
    # User ki saari predictions lo
    predictions = Price_Prediction.objects.filter(user=req.user)
    
    # Total kitni predictions ki
    total_predictions = predictions.count()
    
    # Last prediction
    last_prediction = predictions.last()
    
    context = {
        'tab'              : tab,
        'user_profile'     : user_profile,
        'total_predictions': total_predictions,
        'last_prediction'  : last_prediction,
    }
    return render(req, 'dashboard.html', context)

def user_logout(req):
    is_admin = req.user.is_staff  #  pehle check karo — admin hai?
    req.session.flush()
    auth_logout(req)

    if is_admin:
        return redirect('admin_login')   # 👈 admin login pe bhejo
    else:
        return redirect('login')      # 👈 normal user login pe bhejo
    
@login_required(login_url='login')
def update_photo(req):
    if req.method == 'POST':
        user_profile = UserProfile.objects.get(user=req.user)
        
        #  Photo form se lo
        if 'photo' in req.FILES:
            user_profile.photo = req.FILES['photo']
            user_profile.save()
            messages.success(req, 'Profile picture updated!')
        else:
            messages.error(req, 'Koi photo select nahi ki!')
            
        return redirect('dashboard')
    
def admin_login(req):
    tab = 'admin_login'

    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = authenticate(req, username=username, password=password)

        # ✅ Check — sahi hai aur admin hai?
        if user is not None and user.is_staff:
            auth_login(req, user)
            return redirect('admin_panel')

        # ✅ Login to hua but admin nahi
        elif user is not None and not user.is_staff:
            messages.error(req, 'You are not an admin!')
            return render(req, 'admin_login.html', {'tab': tab})

        # ✅ Wrong username ya password
        else:
            messages.error(req, 'Wrong username or password!')
            return render(req, 'admin_login.html', {'tab': tab})

    return render(req, 'admin_login.html', {'tab': tab})
    
    
# ✅ Admin check karne ka function
def admin_required(view_func):
    def wrapper(req, *args, **kwargs):
        if not req.user.is_staff:  # is_staff = admin hai
            raise PermissionDenied  # access band!
        return view_func(req, *args, **kwargs)
    return login_required(wrapper)


# ✅ Admin Dashboard — sab users dikhao
@admin_required
def admin_panel(req):
    tab = 'admin'
    
    total_users       = User.objects.count()
    total_predictions = Price_Prediction.objects.count()
    all_users         = UserProfile.objects.select_related('user').all()
    
    context = {
        'tab'              : tab,
        'total_users'      : total_users,
        'total_predictions': total_predictions,
        'all_users'        : all_users,
    }
    return render(req, 'admin_panel.html', context)


# ✅ User Detail — ek user ka pura data
@admin_required
def admin_user_detail(req, user_id):
    tab          = 'admin'
    user_obj     = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user_obj)
    predictions  = Price_Prediction.objects.filter(user=user_obj)
    
    context = {
        'tab'         : tab,
        'user_obj'    : user_obj,
        'user_profile': user_profile,
        'predictions' : predictions,
    }
    return render(req, 'admin_user.html', context)

@admin_required
def admin_all_predictions(req):
    tab = 'admin'
    all_predictions = Price_Prediction.objects.select_related('user').all()
    context = {
        'tab'            : tab,
        'all_predictions': all_predictions,
    }
    return render(req, 'admin_all_predictions.html', context)