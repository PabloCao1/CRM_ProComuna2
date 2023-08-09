from django.views.generic import TemplateView,View
from django.views import View
from django.http import JsonResponse
from Eventos.models import Eventos

class CalendarioView(TemplateView):
    template_name = 'calendario/calendario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eventos = Eventos.objects.all().values('id','nombre', 'fecha', 'hora', 'minutos', 'lugar', 'calle', 'altura', 'telefono', 'web', 'modo', 'mensaje', 'flyer')
        context['eventos'] = list(eventos)
        return context

class EventosJsonView(View):
    def get(self, request, *args, **kwargs):
        eventos = Eventos.objects.all().values('id','nombre', 'fecha', 'hora', 'minutos', 'lugar', 'calle', 'altura', 'telefono', 'web', 'modo', 'mensaje', 'flyer')
        return JsonResponse(list(eventos), safe=False)


