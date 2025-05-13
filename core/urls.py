from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm
from .logout import logout_view  # Import from your logout.py file

app_name = 'core'  # This sets the app namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('logout/', logout_view, name='logout'), # Changed to 'logout'
    path('new_item/', views.new_item, name='new_item'),
]