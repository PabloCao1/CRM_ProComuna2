from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('index/',login_required(TemplateView.as_view(template_name='index.html')),name='index'),
]

