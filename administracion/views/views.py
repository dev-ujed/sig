from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import MenuItem
from ..serializers import MenuItemSerializer
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
# Create your views here.

def home(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			print('holi')
		return render(request, 'admin/home.html')

def pdfPuali(request):
    html_string = render_to_string('admin/puali/pdf.html', {'datos': 'valor'})
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