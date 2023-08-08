from django.shortcuts import render
from django.views.generic import TemplateView
from Bases.models import *

class Dashboard(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        perfiles = Perfiles.objects.filter(activo=True)
        general = perfiles.filter(es_fiscal=False,es_voluntario=False).distinct().count()
        voluntarios = perfiles.filter(es_voluntario=True).count()
        fiscales = perfiles.filter(es_fiscal=True).count()

        context = {
                'general': general,
                'voluntarios': voluntarios,
                'fiscales': fiscales,
                }
        return context
