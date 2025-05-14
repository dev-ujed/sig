from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import qrcode
from io import BytesIO
import base64
import json
# Create your views here.

def home(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			print('holi')
		return render(request, 'admin/home.html')

def pdfPuali(request, folio):
    serializer = constPualiSerializer(PUAALI_DATOS_CONSTANCIAS.objects.get(folio = folio)).data
    qr_data = 'https://facultaddelenguas.ujed.mx/puaali/validar-certificado/' + folio
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    qr_uri = f'data:image/png;base64,{qr_base64}'

    html_string = render_to_string('admin/puali/pdf.html', {
        'data': serializer,
        'qr_image': qr_uri
    })

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="documento.pdf"'
    return response

def run():
    inicio = MenuItem.objects.create(id=1, text='Inicio', icon='mdi-home', link='inicio/')
    perfil = MenuItem.objects.create(id=2, text='Perfil', icon='mdi-account', link='perfil/')
    configuracion = MenuItem.objects.create(id=3, text='Configuración', icon='mdi-cog', key='settings')
    labels = MenuItem.objects.create(id=4, text='Labels', icon='mdi-cog', key='labels')

    # Submenús de Configuración
    MenuItem.objects.create(id=5, text='Configuración 1', icon='mdi-account', link='settings1/', parent=configuracion)
    MenuItem.objects.create(id=6, text='Configuración 2', icon='mdi-cog', link='settings2/', parent=configuracion)

    # Submenús de Labels
    MenuItem.objects.create(id=7, text='Label 1', icon='mdi-account', link='label1/', parent=labels)
    MenuItem.objects.create(id=8, text='Label 2', icon='mdi-cog', link='label2/', parent=labels)

    print("✅ Menú insertado correctamente.")