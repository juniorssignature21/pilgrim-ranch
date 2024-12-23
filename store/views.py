from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm
# Create your views here.


def category_summary(request):
        categories = Category.objects.all()
        return render(request, 'store/category_summary.html', {'categories': categories})


def category(request, foo):
    # replace hyphens with spaces
    foo = foo.replace('-', '')
    # Grab the category from the url
    try:
        #look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'store/category.html', {'products': products, 'category': category})
    except:
        messages.success(request, ("That category does not exist!!!"))
        return redirect('home')
    


    

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product.html', {'product': product})    

def home(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def about(request):
    return render(request, 'store/about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been Logged in successfully!!!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error please try again!!!"))
            return redirect('home')
    else:
        return render(request, 'store/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("you have been logged out!!!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("you have registered successfully!!!"))
            return redirect("home")
        else:
            messages.success(request, ("there was a problem registering!!!"))
            return redirect("register")
    else:
        return render(request, 'store/register.html', {"form": form})
    

