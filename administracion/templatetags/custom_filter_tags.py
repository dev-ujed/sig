# menu_tags.py
from django import template
from ..models import MenuItem
from ..serializers import MenuItemSerializer
import json

register = template.Library()

@register.filter()
def get_menu(request):
    print(request)
    menu_items = MenuItem.objects.filter(parent__isnull=True)
    serializer = MenuItemSerializer(menu_items, many=True)
    return json.dumps(serializer.data)
