from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('Usuarios.urls')),
    path('', include('Home.urls')),
    path('', include('Bases.urls')),
    path('', include('Calendario.urls')),
    path('', include('Eventos.urls')),
    path('', include('Comunicaciones.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
