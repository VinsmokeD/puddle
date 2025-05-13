from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import HttpResponseForbidden
from .forms import SignupForm  # Only import what you need
from item.forms import NewItemForm
from item.models import Category, Item

# Homepage view
def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

# Contact page view
def contact(request):
    return render(request, 'core/contact.html')

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:index')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

# Logout view

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('core:index')  # Make sure this matches your index URL name # or your preferred redirect

# New item view (you already had this)
@login_required
def new_item(request):
    if request.user.groups.filter(name='customers').exists():
        return HttpResponseForbidden("You are not allowed to access this page.")

    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('core:index')
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })