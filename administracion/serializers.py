from rest_framework import serializers
from .models import *
from datetime import datetime
import locale

class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'text', 'icon', 'link', 'key', 'children']

    def get_children(self, obj):
        if obj.children.exists():
            return MenuItemSerializer(obj.children.all(), many=True).data
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {key: value for key, value in representation.items() if value is not None}

class constPualiSerializer(serializers.ModelSerializer):
    nivel_explicacion   = serializers.SerializerMethodField()
    fecha_hoy           = serializers.SerializerMethodField()
    tipo_constancia     = serializers.SerializerMethodField()
    calificacion_letra  = serializers.SerializerMethodField()
    fecha_texto         = serializers.SerializerMethodField()
    class Meta:
        model = PUAALI_DATOS_CONSTANCIAS
        fields = '__all__'
        
    def get_nivel_explicacion(self, obj):
        explicacion = OpuaaliNivel.objects.get(nivel = obj.nivel)
        return explicacion.nivel_explicacion
    
    def get_fecha_hoy(self, obj):
        locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
        fecha_actual = datetime.now()
        fecha_formateada = f"Se extiende la presente a los {fecha_actual.day} días del mes de {fecha_actual.strftime('%B')} de {fecha_actual.year}."
        return fecha_formateada
    
    def get_tipo_constancia(self, obj):
        tipo = PUAALI_TIPOS_CONSTANCIAS.objects.get(tipo_constancia_id = obj.tipo_constancia_id.tipo_constancia_id)
        return tipo.tipo_constancia_desc
    
    def get_calificacion_letra(selg, obj):
        from decimal import Decimal, ROUND_DOWN
        from num2words import num2words

        calificacion_decimal = Decimal(obj.calificacion).quantize(Decimal("0.0"), rounding=ROUND_DOWN)
        entero = int(calificacion_decimal)
        decimal = int(str(calificacion_decimal).split('.')[1])
        calificacion_letra = f"{num2words(entero, lang='es')} punto {num2words(decimal, lang='es')}"

        return f"{calificacion_decimal} ({calificacion_letra})"
    
    def get_fecha_texto(self, obj):
        fecha = obj.fecha 
        return fecha.strftime("en el mes de %B del %Y")