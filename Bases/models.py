from datetime import date
from django.db import models
from django.forms import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from .choices import *
    

class Perfiles(models.Model):
    '''
    Guardado de los perfiles de los vecinos y vecinas del Municipio, principalmente los datos personales.
    ''' 
    apellidos           = models.CharField(max_length=250, null=True, blank=True)    
    nombres             = models.CharField(max_length=250, null=True, blank=True)    
    fecha_nacimiento    = models.DateField(null=True, blank=True)    
    tipo_doc            = models.CharField(max_length=10, choices=CHOICE_TIPO_DOC, default='DNI', null=True, blank=True)      
    documento           = models.PositiveBigIntegerField(validators=[MinValueValidator(3000000), MaxValueValidator(99999999)], unique=True)      
    sexo                = models.CharField(max_length=10, choices=CHOICE_SEXO)      
    nacionalidad        = models.CharField(max_length=15, choices=CHOICE_NACIONALIDAD, default='Argentina', null=True, blank=True)    
    calle               = models.CharField(max_length=100, null=True, blank=True)
    altura              = models.PositiveSmallIntegerField(null=True, blank=True)
    piso                = models.CharField(max_length=10, null=True, blank=True)
    departamento        = models.CharField(max_length=10, null=True, blank=True)
    barrio              = models.CharField(max_length=50, choices= CHOICE_BARRIOS, null=True, blank=True)
    comuna              = models.CharField(max_length=50, choices=CHOICE_COMUNAS, null=True, blank=True)
    provincia           = models.CharField(max_length=50, choices=CHOICE_PROVINCIAS, default='CABA')
    telefono            = models.PositiveIntegerField(null=True, blank=True)
    email               = models.EmailField(null=True, blank=True)
    instagram           = models.CharField(max_length=20, null=True, blank=True)
    facebook            = models.CharField(max_length=20, null=True, blank=True)
    observaciones       = models.CharField(max_length=300,blank=True,null=True)
    es_empleadoGCBA     = models.BooleanField(default=False,blank=True,null=True)
    es_militante        = models.BooleanField(default=False,blank=True,null=True)
    es_voluntario       = models.BooleanField(default=False,blank=True,null=True)
    es_fiscal           = models.BooleanField(default=False,blank=True,null=True)
    activo              = models.BooleanField(default=True)
    motivo_inactivo     = models.CharField(max_length=100,blank=True,null=True)
    fecha_ingreso       = models.DateField(default=date.today())
    creado              = models.DateField(auto_now_add=True)
    modificado          = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"
    
    class Meta:
        ordering = ['-fecha_ingreso']
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def edad(self):
        today = date.today()
        if self.fecha_nacimiento:
            age = today.year - self.fecha_nacimiento.year
            if today.month < self.fecha_nacimiento.month or (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
                age -= 1
            return age
        return None

    def get_absolute_url(self):
        return reverse('perfiles_ver', kwargs={'pk': self.pk})


    
class BaseVoluntariosPerfiles(models.Model):
    fk_perfil_v = models.ForeignKey(Perfiles, on_delete=models.CASCADE, null=True, blank=True)
    grupo_wsp   = models.BooleanField(blank=True,null=True)
    gen_23      = models.BooleanField(blank=True,null=True)
    eventos     = models.BooleanField(blank=True,null=True)
    afinidad    = models.CharField(max_length=50, null=True, blank=True, choices=CHOICE_AFINIDAD)
    otro_afinidad    = models.CharField(max_length=50, null=True, blank=True)
    equipo_futbol = models.CharField(max_length=50, null=True, blank=True, choices=CHOICE_EQUIPO_FUTBOL)
    observaciones_v = models.CharField(max_length=300,blank=True,null=True)
    creado        = models.DateField(auto_now_add=True)
    modificado    = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'BaseVoluntariosPerfil'
        verbose_name_plural = 'BaseVoluntariosPerfiles'

    def get_absolute_url(self):
        return reverse('basevoluntariosperfil_ver', kwargs={'pk': self.pk})


class BaseFiscalesPerfiles(models.Model):
    fk_perfil_f       = models.ForeignKey(Perfiles, on_delete=models.CASCADE, null=True, blank=True)
    fue_fiscal      = models.BooleanField(null=True, blank=True)
    fecha_fiscal    = models.DateField(null=True, blank=True, )
    rol_fiscal      = models.CharField(max_length=50, null=True, blank=True, choices=CHOICE_ROL_FISCAL)
    disp_jornada    = models.CharField(max_length=50, null=True, blank=True, choices=CHOICE_DISP_JORNADA)
    desempeno       = models.CharField(max_length=50, null=True, blank=True, choices=CHOICE_FISCAL_DESEMPENO)
    observaciones_f   = models.CharField(max_length=300,blank=True,null=True)
    creado          = models.DateField(auto_now_add=True)
    modificado      = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'BaseFiscalesPerfil'
        verbose_name_plural = 'BaseFiscalesPerfiles'

    def get_absolute_url(self):
        return reverse('basefiscalesperfil_ver', kwargs={'pk': self.pk})
