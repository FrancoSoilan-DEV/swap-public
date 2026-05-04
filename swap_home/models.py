from django.db import models
from swap_porteria.models import *
from swap_tthh.models import *

    
# --- Tareas ---

class Tareadia(models.Model):
    td_id = models.AutoField(primary_key=True)
    td_dia = models.CharField(max_length=45, verbose_name="Dia")
    class Meta:
        #managed = False
        db_table = 'tareadia'
        verbose_name = "Dia de la Tarea"
        verbose_name_plural = "Dias de las Tareas"
        #ordering = ["td_dia"]
    def __str__(self):
        return f"{self.td_dia}"

class Tareaestado(models.Model):
    te_id = models.AutoField(primary_key=True)
    te_estado = models.CharField(max_length=45, verbose_name="Estado")
    class Meta:
        #managed = False
        db_table = 'tareaestado'
        verbose_name = "Estado de Tarea"
        verbose_name_plural = "Estados de Tareas"
        ordering = ["te_estado"]
    def __str__(self):
        return f"{self.te_estado}"

class Tareas(models.Model):
    tarea_id = models.AutoField(primary_key=True)  # The composite primary key (tarea_id, tarea_dpto_id, tarea_te_id, tarea_td_id) found, that is not supported. The first column is selected.
    tarea_titulo = models.CharField(max_length=50, verbose_name="Titulo de Tarea")
    tarea_descripcion = models.CharField(max_length=250, blank=True, null=True, verbose_name="Descripcion de Tarea")
    tarea_dpto = models.ForeignKey(Departamentos, models.DO_NOTHING, verbose_name="Departamento Pertinente")
    tarea_te = models.ForeignKey(Tareaestado, models.DO_NOTHING, verbose_name="Estado de la Tarea")
    tarea_td = models.ForeignKey(Tareadia, models.DO_NOTHING, verbose_name="Dia de la Tarea")
    class Meta:
       # managed = False
        db_table = 'tareas'
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["tarea_titulo"]
    def __str__(self):
        return f"{self.tarea_titulo}"

# ===============================================================================================================================
# ===============================================================================================================================


