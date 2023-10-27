from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'opeapp'

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False), name='index'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]