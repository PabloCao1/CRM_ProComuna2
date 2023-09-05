from django.contrib import admin
from .models import *
from import_export import resources, fields

class PerfilesResource(resources.ModelResource):
    activo = fields.Field()
    es_fiscal = fields.Field()
    es_militante = fields.Field()
    es_voluntario = fields.Field()
    es_empleadoGCBA = fields.Field()
    matriculado = fields.Field()
    socio_futbol = fields.Field()
    fecha_nacimiento = fields.Field()
    fecha_inactivo = fields.Field()
    creado = fields.Field()

    class Meta:
        model = Perfiles
        exclude = ('modificado','id')

    def dehydrate_activo(self, obj):
        return 'SI' if obj.activo else 'NO'
    def dehydrate_es_fiscal(self, obj):
        return 'SI' if obj.es_fiscal else 'NO'
    def dehydrate_es_militante(self, obj):
        return 'SI' if obj.es_militante else 'NO'
    def dehydrate_es_voluntario(self, obj):
        return 'SI' if obj.es_voluntario else 'NO'
    def dehydrate_es_empleadoGCBA(self, obj):
        return 'SI' if obj.es_empleadoGCBA else 'NO'
    def dehydrate_matriculado(self, obj):
        return 'SI' if obj.matriculado else 'NO'
    def dehydrate_socio_futbol(self, obj):
        return 'SI' if obj.socio_futbol else 'NO'
    def dehydrate_creado(self, obj):
        return obj.creado.strftime("%d-%m-%Y")
    def dehydrate_fecha_inactivo(self, obj):
        return obj.fecha_inactivo.strftime("%d-%m-%Y") if obj.fecha_inactivo else '-'
    def dehydrate_fecha_nacimiento(self, obj):
        return obj.fecha_nacimiento.strftime("%d-%m-%Y") if obj.fecha_nacimiento else '-'

admin.site.register(Perfiles)