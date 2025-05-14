from django.urls import path, include
from  administracion.views import views, unidad, profesor

urlpatterns = [
	path('', views.home, name='home' ),
	path('puali/pdf/<str:folio>/', views.pdfPuali, name='pdf-puali' ),
]