from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django .contrib import messages
from datetime import datetime

#----------- VIEW CALENDARIO --------------------------

def Calendario(request):
   anio = datetime.now().date()
   year = anio.year
   
   data = {
      }   
   
   return render(request,'calendario/calendario.html', data)


