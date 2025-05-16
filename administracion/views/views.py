from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import *
from ..serializers import *
from django.template.loader import render_to_string
from weasyprint import HTML
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Case, When, IntegerField, F, Q
from rest_framework import status
from datetime import datetime
from django.db.models import Max
from django.db.models.functions import Coalesce
import hashlib
import random
import json
# Create your views here.

def home(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			print('holi')
		return render(request, 'admin/home.html')
	
def certificadosIndex(request):
    if request.method == 'GET':
        return render(request, 'admin/certificados/index.html')
        
def certificadosForm(request):
    if request.method == 'GET':
        return render(request, 'admin/certificados/formCertificados.html')

def getEscuelas(request):
	if request.method == 'GET':
		escuelas_licenciatura = Ocarreras.objects.filter(
            cve_carrera__gte="140000",
            cve_carrera__lte="149999"
        ).values_list('cve_escuela', flat=True).distinct()



		escuelas = Oescuelas.objects.annotate(
            orden=Case(
                When(cve_escuela__in=escuelas_licenciatura, then=0),
                default=1,
                output_field=IntegerField()
            ),
			escuela_imprime_contenido=Coalesce('escuela_imprime', F('desc_escuela'))
        ).order_by('orden', 'desc_completo').values("cve_escuela", "desc_escuela", "escuela_imprime_contenido")

		data_escuelas = list(escuelas)

		return JsonResponse(data_escuelas, safe=False)
	
def getPuaali_datos_contancias(request):
    if(request.method == 'GET'):
        buscar = request.GET.get('buscar', '').strip().upper()
        #datos = PUAALI_DATOS_CONSTANCIAS.objects.all().values('folio', 'nombre_alumno', 'tipo_constancia_id', 'nivel', 'cve_escuela', 'fecha')
        datos = PUAALI_DATOS_CONSTANCIAS.objects.select_related('tipo_constancia_id', 'cve_escuela').values('folio','nombre_alumno','nivel','calificacion','fecha',tipo_constancia_desc=F('tipo_constancia_id__tipo_constancia_desc'),escuela=F('cve_escuela__desc_escuela'))
        resultado = []

        if buscar:
            datos = datos.filter(
                Q(nombre_alumno__icontains=buscar) | Q(folio__icontains=buscar)
            )

        datos = datos.order_by('-fecha')

        page_number = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        paginator = Paginator(list(datos), page_size)
        page = paginator.get_page(page_number)

        response_data = {
            'constancias': list(page.object_list),
            'total_pages': paginator.num_pages,
            'current_pages': page.number,
            'total_items': paginator.count
        }

        return JsonResponse(response_data, safe=False)
	
def getTiposConstancias(request):
	if(request.method == 'GET'):
		tipos_constancias = PUAALI_TIPOS_CONSTANCIAS.objects.all().values()
		print(tipos_constancias)

		return JsonResponse(list(tipos_constancias), safe=False)
	
class generarConstancia(APIView):
    def post(self, request):
        try:
            # Obtener datos del request
            nombre = request.data.get("nombre")
            tipo_constancia_id = request.data.get("tipoConstancia")
            nivel = request.data.get("nivel")
            calificacion = request.data.get("calificacion")
            cve_escuela = request.data.get("escuela")
            fecha = request.data.get("fecha")

            tipo_constancia = PUAALI_TIPOS_CONSTANCIAS.objects.get(pk=tipo_constancia_id)
            escuela = Oescuelas.objects.get(pk=cve_escuela)

            año_actual = datetime.now().year
            prefijo_folio = f"{año_actual}"

            ultimo_folio_del_año = (
                PUAALI_DATOS_CONSTANCIAS.objects
                .filter(folio__startswith=prefijo_folio)
                .aggregate(max_folio=Max('folio'))['max_folio']
            )

            if ultimo_folio_del_año:
                # Incrementar el último folio
                nuevo_numero = int(str(ultimo_folio_del_año)[4:]) + 1
            else:
                # Si no hay folios de este año, empezar en 1
                nuevo_numero = 1

            nuevo_folio = int(f"{año_actual}{nuevo_numero:05d}")

            texto_hash = f"{nuevo_folio}{random.randint(1000,9999)}"
            hash_generado = hashlib.sha256(texto_hash.encode()).hexdigest()

            marco_generado = "MCER (Marco Común Europeo de Referencia para las Lenguas)"

            nueva_constancia = PUAALI_DATOS_CONSTANCIAS(
                folio=nuevo_folio,
                nombre_alumno=nombre,
                tipo_constancia_id=tipo_constancia,
                nivel=nivel,
                marco=marco_generado,
                calificacion=calificacion,
                cve_escuela=escuela,
                fecha=fecha,
                hash=hash_generado,
            )

            print(nueva_constancia)

            nueva_constancia.save()
    
            return Response({
                "message": "Constancia generada exitosamente.",
                "folio": nuevo_folio,
                "hash": hash_generado
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, folio):
        try:
            if not folio:
                return Response({"error": "Folio requerido para editar."}, status=status.HTTP_400_BAD_REQUEST)

            constancia = PUAALI_DATOS_CONSTANCIAS.objects.get(folio=folio)

            constancia.nombre_alumno = request.data.get("nombre", constancia.nombre_alumno)

            tipo_constancia_id = request.data.get("tipoConstancia")
            if tipo_constancia_id:
                constancia.tipo_constancia_id = PUAALI_TIPOS_CONSTANCIAS.objects.get(pk=tipo_constancia_id)

            constancia.nivel = request.data.get("nivel", constancia.nivel)
            constancia.calificacion = request.data.get("calificacion", constancia.calificacion)

            escuela_id = request.data.get("escuela")
            if escuela_id:
                constancia.cve_escuela = Oescuelas.objects.get(pk=escuela_id)

            constancia.fecha = request.data.get("fecha", constancia.fecha)
            constancia.save()

            return Response({"message": "Constancia actualizada exitosamente."}, status=status.HTTP_200_OK)

        except PUAALI_DATOS_CONSTANCIAS.DoesNotExist:
            return Response({"error": "Constancia no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, folio):
        try:
            constancia = get_object_or_404(PUAALI_DATOS_CONSTANCIAS, folio=folio)
            return Response({
                "folio": constancia.folio,
                "nombre_alumno": constancia.nombre_alumno,
                "tipo_constancia": constancia.tipo_constancia_id.tipo_constancia_id,  
                "nivel": constancia.nivel,
                "calificacion": constancia.calificacion,
                "escuela": constancia.cve_escuela.cve_escuela,
                "fecha": constancia.fecha,
                "fecha_creacion": constancia.fecha_creacion,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class eliminarConstancia(APIView):
    def delete(self, request, folio):
        try:
            constancia = get_object_or_404(PUAALI_DATOS_CONSTANCIAS, folio=folio)
            constancia.delete()
            return Response({"message": "Constancia eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
def pdfCertiPuali(request, folio):
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