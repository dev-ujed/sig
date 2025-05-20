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

class Rol(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
    
class MenuRol(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.email} -> {self.menu_item.text}"

class MenuPermission(models.Model):
    email = models.CharField(max_length=120, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('email', 'rol')

    def __str__(self):
        return f"{self.email} -> {self.rol.name}"
    
class Oescuelas(models.Model):
    cve_escuela = models.CharField(primary_key=True, max_length=10)
    desc_escuela = models.CharField(max_length=120)
    desc_completo = models.CharField(max_length=100)
    desc_corto = models.CharField()
    escuela_imprime = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=30)
    class Meta:
        managed     = False
        db_table    = '"DESARROLLO"."ESCUELA"'
        app_label   = 'desarrollo'
        
class Ocarreras(models.Model):
    cve_carrera = models.CharField(primary_key=True, max_length=8)
    desc_carrera = models.CharField(max_length=60)
    activa = models.CharField(max_length=10)
    cve_escuela = models.ForeignKey(Oescuelas, on_delete=models.CASCADE, null=True, db_column='CVE_ESCUELA')
    class Meta:
        managed     = False
        db_table    = '"DESARROLLO"."CARRERA"'
        app_label   = 'desarrollo'
        
class PUAALI_TIPOS_CONSTANCIAS(models.Model):
    tipo_constancia_id = models.IntegerField(primary_key=True)
    tipo_constancia_desc = models.CharField(max_length=30)
    activo = models.CharField(max_length=2)
    class Meta:
        managed = False
        db_table = '"DESARROLLO"."PUAALI_TIPOS_CONSTANCIAS"'
        app_label = 'desarrollo'
        
class PUAALI_DATOS_CONSTANCIAS(models.Model):
    folio = models.IntegerField(primary_key=True)
    nombre_alumno = models.CharField(max_length=70)
    tipo_constancia_id = models.ForeignKey(PUAALI_TIPOS_CONSTANCIAS, on_delete=models.CASCADE, db_column='tipo_constancia_id')
    nivel = models.CharField(max_length=5)
    marco = models.CharField(max_length=60)
    calificacion = models.FloatField()
    cve_escuela = models.ForeignKey(Oescuelas, on_delete=models.CASCADE, db_column='cve_escuela')
    fecha = models.DateField()
    hash = models.CharField(max_length=100, unique=True)
    fecha_creacion = models.DateField(auto_now=True)
    class Meta:
        managed = False
        db_table = '"DESARROLLO"."PUAALI_DATOS_CONSTANCIAS"'
        app_label = 'desarrollo'
        
class OpuaaliNivel(models.Model):
    cve_nivel           = models.IntegerField(primary_key=True)
    nivel               = models.CharField(max_length = 10)
    descripcion         = models.CharField(max_length = 50)
    tipo                = models.CharField(max_length = 50)
    tipo_constancia_id  = models.IntegerField()
    nivel_explicacion   = models.CharField(max_length = 800)
    
    class Meta:
        managed = False
        db_table = '"DESARROLLO"."PUAALI_NIVEL"'
        app_label = 'desarrollo'