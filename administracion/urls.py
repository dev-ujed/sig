from django.urls import path, include
from  administracion.views import views, unidad, profesor
from administracion.views.views import generarConstancia, eliminarConstancia

urlpatterns = [
	path('', views.home, name='home' ),
	path('unidad/', unidad.index, name='unidad' ),
	path('profesor/', profesor.index, name='profesor' ),
    path('certificado/', views.certificadosIndex, name='certificado'),
    path('certificado/form/', views.certificadosForm, name='certificadosForm'),
    path('escuelas/', views.getEscuelas, name='get_escuelas'),
    path('datos_constancias/', views.getPuaali_datos_contancias, name='get_datos_constancias'),
    path('tipos_constancias/', views.getTiposConstancias, name='getTiposConstancias'),
    path('generar_certificado/', generarConstancia.as_view(), name='generar_certificado'),
    path('get_constancia/<int:folio>/', generarConstancia.as_view(), name='get_constancia'),
    path('update_constancia/<int:folio>/', generarConstancia.as_view(), name='get_constancia'),
	path('delete_constancia/<int:folio>/', eliminarConstancia.as_view(), name='eliminar_constancia'),
]