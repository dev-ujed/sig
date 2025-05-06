from rest_framework import serializers
from .models import *

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