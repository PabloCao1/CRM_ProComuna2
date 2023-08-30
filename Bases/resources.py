
import xlwt
from django.http import HttpResponse
from .models import *

def export_to_xls(queryset):
    '''
    Genera y descarga un excel con todos los campos del modelo Perfiles y sus campos vinculados en los modelos BaseVoluntariosPerfiles y BaseFiscalesPerfiles
    '''

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="CRM_info_completa.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Perfiles')

    # Estilo para la primera fila (nombres de columna)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    font.height = 12 * 20  # Tamaño de fuente en unidades de 1/20 de punto (14pt)
    style.font = font
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
    style.pattern = pattern

    row_num = 0

    columns = [
        "Ingreso a la Base",
        "Estado",
        "Apellidos",
        "Nombres",
        "Fecha de Nacimiento",
        "Edad",
        "Tipo de Documento",
        "Documento",
        "Sexo",
        "Nacionalidad",
        "Domicilio",
        "Teléfono",
        "Email",
        "Instagram",
        "Facebook",
        "Equipo Fútbol",
        "Es socio del Club",
        "Profesión",
        "Es Matriculado",
        "Es Empleado GCBA",
        "Es Militante",
        "Está en Base Voluntarios",
        "Está en Base Fiscales",
        "Fecha desactivación",
        "Motivo desactivación",
        "Obervaciones del Perfil",

        #Base Voluntarios
        "Fecha ingreso como Voluntario",
        "Está en Grupo WhatsApp",
        "Está en Gen 23",
        "Participa en eventos del local",
        "Afinidad",
        "Otra Afinidad",
        "Observaciones B. Voluntarios",
        
        #Base Fiscales
        "Fecha ingreso como Fiscal",
        "Fue Fiscal",
        "Última Fecha Fiscal",
        "Rol ejercido",
        "Disponibilidad",
        "Desempeño",
        "Observaciones B. Fiscales",
    ]

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, style)

    for obj in queryset:
        row_num += 1
        row = [
            obj.creado.strftime("%d/%m/%Y"),
            'ACTIVO' if obj.activo else 'DESACTIVADO',
            obj.apellidos if obj.apellidos else '',
            obj.nombres if obj.nombres else '',
            obj.fecha_nacimiento.strftime("%d/%m/%Y") if obj.fecha_nacimiento else '',
            str(obj.edad()) + " años" if obj.edad() else '',
            obj.tipo_doc if obj.tipo_doc else '',
            obj.documento if obj.documento else '',
            obj.sexo if obj.sexo else '',
            obj.nacionalidad if obj.nacionalidad else '',
            obj.direccion_completa() if obj.direccion_completa() else '',
            obj.telefono if obj.telefono else '',
            obj.email if obj.email else '',
            obj.instagram if obj.instagram else '',
            obj.facebook if obj.facebook else '',
            obj.equipo_futbol if obj.equipo_futbol else '',
            'SI' if obj.socio_futbol else 'NO',
            obj.profesion if obj.profesion else '',
            'SI' if obj.matriculado else 'NO',
            'SI' if obj.es_empleadoGCBA else 'NO',
            'SI' if obj.es_militante else 'NO',
            'SI' if obj.es_voluntario else 'NO',
            'SI' if obj.es_fiscal else 'NO',
            obj.fecha_inactivo.strftime("%d/%m/%Y") if obj.fecha_inactivo else '',
            obj.motivo_inactivo if obj.motivo_inactivo else '',
            obj.observaciones if obj.observaciones else '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
            '',
        ]
        
        # Lógica para obtener los objetos relacionados
        voluntarios_perfiles = BaseVoluntariosPerfiles.objects.filter(fk_perfil_v=obj)
        fiscales_perfiles = BaseFiscalesPerfiles.objects.filter(fk_perfil_f=obj)
        
        if voluntarios_perfiles.exists():
            voluntario = voluntarios_perfiles.first()
            row[26] = voluntario.creado.strftime("%d/%m/%Y")
            row[27] = 'SI' if voluntario.grupo_wsp else 'NO'
            row[28] = 'SI' if voluntario.gen_23 else 'NO'
            row[29] = 'SI' if voluntario.eventos else 'NO'
            row[30] = voluntario.afinidad if voluntario.afinidad else ''
            row[31] = voluntario.otro_afinidad if voluntario.otro_afinidad else ''
            row[32] = voluntario.observaciones_v if voluntario.observaciones_v else ''
        
        if fiscales_perfiles.exists():
            fiscal = fiscales_perfiles.first()
            row[33] = fiscal.creado.strftime("%d/%m/%Y")
            row[34] = 'SI' if fiscal.fue_fiscal else 'NO'
            row[35] = fiscal.fecha_fiscal.strftime("%d/%m/%Y") if fiscal.fecha_fiscal else ''
            row[36] = fiscal.rol_fiscal if fiscal.rol_fiscal else ''
            row[37] = fiscal.disp_jornada if fiscal.disp_jornada else ''
            row[38] = fiscal.desempeno if fiscal.desempeno else ''
            row[39] = fiscal.observaciones_f if fiscal.observaciones_f else ''
            
        
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, cell_value)

    wb.save(response)
    return response