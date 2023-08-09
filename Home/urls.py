from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('dashboard/',login_required(Dashboard.as_view()),name='index'),
    path('error500/', login_required(TemplateView.as_view(template_name='500.html')), name='500'),
    path('error404/', login_required(TemplateView.as_view(template_name='404.html')), name='404'),
    path('error403/', login_required(TemplateView.as_view(template_name='403.html')), name='403'),
]

