from django.db import models

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