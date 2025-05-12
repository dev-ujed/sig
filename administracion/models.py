from django.db import models
from public.models import CustomUser

class MenuItem(models.Model):
    text = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    key = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.text
    
class MenuPermission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='menu_permissions')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='user_permissions')

    class Meta:
        unique_together = ('user', 'menu_item')

    def __str__(self):
        return f"{self.user.email} -> {self.menu_item.text}"
