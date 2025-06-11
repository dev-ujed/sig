# menu_tags.py
from django import template
from ..models import *
from ..serializers import *
from django.db.models import Q
from django.template.defaultfilters import register
import json
import os
from django.conf import settings

register = template.Library()

@register.filter()
def get_menu(request):
    if MenuPermission.objects.filter(email = request.user.email, rol_id = 1).exists():
        menu_items = MenuItem.objects.exclude(parent__isnull=False).distinct()
    else:
        roles = MenuPermission.objects.filter(email = request.user.email).values_list('rol')
        menu_rol = MenuRol.objects.filter(rol__in = roles).values_list('menu_item')
        menu_items = MenuItem.objects.filter(Q(id=1) | Q(parent__isnull=True, id__in = menu_rol)).distinct()
        
    serializer = MenuItemSerializer(menu_items, many=True)
    
    return json.dumps(serializer.data)

