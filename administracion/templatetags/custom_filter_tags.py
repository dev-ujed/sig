# menu_tags.py
from django import template
from ..models import MenuItem
from ..serializers import MenuItemSerializer
import json
from django.db.models import Q

register = template.Library()

@register.filter()
def get_menu(request):
    print(request)
    menu_items = MenuItem.objects.filter(Q(id=1) | Q(parent__isnull=True, user_permissions__user=request.user)).distinct()
    serializer = MenuItemSerializer(menu_items, many=True)
    return json.dumps(serializer.data)
