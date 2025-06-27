from django.db import models
from swap_porteria.models import *
from swap_tthh.models import *
# Create your models here.
# ===============================================================================================================================
# ===============================================================================================================================
from django.contrib.auth.models import User  # Importás el modelo User
# Servicio Tecnico
    


class Tecnicosmonto(models.Model):
    tm_id = models.SmallAutoField(primary_key=True)
    tm_monto = models.IntegerField(verbose_name="Monto")
    class Meta:
        #managed = False
        db_table = 'tecnicosmonto'
        verbose_name = "Monto"
        verbose_name_plural = "Montos"
        ordering = ["tm_monto"]
    def __str__(self):
        return f"{self.tm_monto}"




class Tecnicos(models.Model):
    tec_id = models.BigAutoField(primary_key=True)
    tec_fexacta = models.DateField(verbose_name="Fecha Exacta")
    tec_hexacta = models.TimeField(verbose_name="Hora Exacta")
    tec_sitios = models.CharField(max_length=60, blank=True, null=True, verbose_name="Sitio")
    tec_cliente = models.CharField(max_length=60, verbose_name="Cliente")
    tec_descripcion = models.CharField(max_length=250, verbose_name="Descripcion")
    tec_fecha = models.DateField(verbose_name="Fecha de Realizacion del Trabajo")
    tec_hinicio = models.TimeField(verbose_name="Hora de inicio del Trabajo")
    tec_hfinal = models.TimeField(verbose_name="Hora de Finalizacion del Trabajo")
    tec_ee = models.ForeignKey(Estadoentrada, models.DO_NOTHING,verbose_name="Estado")
    tec_tm = models.ForeignKey('Tecnicosmonto', models.DO_NOTHING, verbose_name="Monto")
    tec_nombre = models.CharField(max_length=250, verbose_name="Nombre del Tecnico")
    class Meta:
        #managed = False
        db_table = 'tecnicos'
        verbose_name = "Tecnico"
        verbose_name_plural = "Tecnicos"
        ordering = ["tec_fecha"]
    def  __str__(self):
        return f"{self.tec_nombre} | {self.tec_fecha}"

