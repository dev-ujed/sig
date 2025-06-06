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


@register.filter()
def menu(request):
    dbmenu = []
    if request.user.is_authenticated:
        dbmenu = [
            {
                'id': 1,
                'ordered': 1,
                'name': 'Declaraciones',
                'slug': 'declaraciones',
                'tile': 'solicitudes.svg',
                'active': 1,
                'submenus' : [
                    {
                        'id': 1,
                        'ordered': 1,
                        'name': 'Mis declaraciones',
                        'searchable_name': 'mis-declaraciones',
                        'icon': 'solicitudes.svg',
                        'active': 1,
                        'links' : [
                            {
                                'id': 1,
                                'ordered': 1,
                                'name': 'Mis declaraciones',
                                'slug': 'mis-declaraciones',
                                'route': 'mis-declaraciones',
                                'active': 0,
                            },
                            {
                                'id': 2,
                                'ordered': 2,
                                'name': 'Declaraciones extemporáneas',
                                'slug': 'declaraciones-pendientes',
                                'route': 'declaraciones-pendientes',
                                'active': 0,
                            },
                            {
                                'id': 3,
                                'ordered': 3,
                                'name': 'Nueva declaración',
                                'slug': 'nueva-declaracion',
                                'route': 'nueva-declaracion',
                                'active': 0,
                            },
                        ]
                    },
                ]
            },
            {
                'id': 2,
                'ordered': 2,
                'name': 'Ayuda',
                'slug': 'ayuda',
                'tile': 'lifeguard.png',
                'active': 0,
                'submenus' : [
                    {
                        'id': 1,
                        'ordered': 1,
                        'name': 'Ayuda',
                        'searchable_name': 'ayuda',
                        'icon': 'question.png',
                        'active': 0,
                        'links' : [
                            {
                                'id': 1,
                                'ordered': 1,
                                'name': 'Llenar declaraciones',
                                'slug': 'llenar-declaraciones',
                                'route': 'llenar-declaraciones',
                                'active': 0,
                            },

                        ]
                    },
                ]
            },
        ]

        menu_admon = {
            'id': 3,
            'ordered': 3,
            'name': 'ACL',
            'slug': 'acl',
            'tile': 'auth.svg',
            'active': 0,
            'submenus' : [
                {
                    'id': 1,
                    'ordered': 1,
                    'name': 'Usuarios',
                    'searchable_name': 'usuarios',
                    'icon': 'user.svg',
                    'active': 0,
                    'links' : [
                        {
                            'id': 1,
                            'ordered': 1,
                            'name': 'Usuarios declaraciones',
                            'slug': 'usuarios-declaraciones',
                            'route': 'usuarios-declaraciones',
                            'active': 0,
                        },
                        {
                            'id': 2,
                            'ordered': 2,
                            'name': 'Modificar usuarios',
                            'slug': 'modificar-usuarios',
                            'route': 'modificar-usuarios',
                            'active': 0,
                        },

                    ]
                },
            ]
        },
        if request.user.groups.filter(name='Administrador').exists():
            dbmenu = list(dbmenu) + list(menu_admon)
    return dbmenu

@register.simple_tag
def vite_assets(path):
    manifest_path = os.path.join(settings.BASE_DIR, 'dist', '.vite', 'mix-manifest.json')

    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        entry = manifest.get(path)

        if not entry:
            return settings.STATIC_URL + path  

        versioned_file = entry.get('file')

        if versioned_file:
            return settings.STATIC_URL + versioned_file.lstrip('/')

        return settings.STATIC_URL + path
    
    except FileNotFoundError:
        return settings.STATIC_URL + path