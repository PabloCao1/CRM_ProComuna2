from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from Bases.models import *


class Dashboard(LoginRequiredMixin,TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        perfiles = Perfiles.objects.all()
        perfiles_activos = perfiles.filter(activo=True)
        general = perfiles_activos.filter(es_fiscal=False,es_voluntario=False).distinct().count()
        voluntarios = perfiles_activos.filter(es_voluntario=True).count()
        fiscales = perfiles_activos.filter(es_fiscal=True).count()

        context = {

                'general': general,
                'voluntarios': voluntarios,
                'fiscales': fiscales,
                'total': perfiles.count(),
                'activos': perfiles_activos.count(),
                'desactivados': perfiles.count() - perfiles_activos.count(),
                }

        return context

