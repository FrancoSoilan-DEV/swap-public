from django.db import models

# Create your models here.
# ===============================================================================================================================
# ===============================================================================================================================
    
# Porteria

class Cobrador(models.Model):
    cob_id = models.SmallAutoField(primary_key=True)
    cob_nombre = models.CharField(max_length=200, verbose_name="Nombre del Cobrador")
    cob_estado = models.CharField(max_length=50, verbose_name="Estado del Cobrador (activo/inactivo)")
    class Meta:
       # managed = False
        db_table = 'cobrador'
        verbose_name = "Cobrador"
        verbose_name_plural = "Cobradores"
        ordering = ["cob_nombre"]
    def __str__(self):
        return f"{self.cob_nombre}"

class Entrada(models.Model):
    e_id = models.BigAutoField(primary_key=True)
    e_fecha = models.DateField(verbose_name="Fecha")
    e_entrada = models.TimeField(verbose_name="Entrada")
    e_salida = models.TimeField(verbose_name="Salida")
    e_fun = models.ForeignKey('swap_tthh.Funcionarios', models.DO_NOTHING, blank=True, null=True,verbose_name="Funcionario")
    e_prov = models.ForeignKey('Proveedor', models.DO_NOTHING, blank=True, null=True,verbose_name="Proveedor")
    e_cob = models.ForeignKey(Cobrador, models.DO_NOTHING, blank=True, null=True,verbose_name="Cobrador")
    e_ee = models.ForeignKey('Estadoentrada', models.DO_NOTHING,verbose_name="Estado")
    e_visita = models.CharField(max_length=200, blank=True, null=True,verbose_name="Visita")
    e_comentario = models.CharField(max_length=45, blank=True, null=True,verbose_name="Comentario")
    class Meta:
        #managed = False
        db_table = 'entrada'
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"
        ordering = ["e_fecha"]
    def __str__(self):
        return f"{self.e_fecha} | {self.e_fun} | {self.e_cob} | {self.e_prov} | {self.e_visita} | {self.e_ee}"

class Estadoentrada(models.Model):
    ee_id = models.AutoField(primary_key=True)
    ee_estado = models.CharField(max_length=50,verbose_name="Estado")
    class Meta:
       # managed = False
        db_table = 'estadoentrada'
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ["ee_estado"]
    def __str__(self):
        return f"{self.ee_estado}"

class Proveedor(models.Model):
    prov_id = models.SmallAutoField(primary_key=True)
    prov_nombre = models.CharField(max_length=200, verbose_name="Nombre del Proveedor")
    prov_estado = models.CharField(max_length=50, verbose_name="Estado del Proveedor (activo/inactivo)")
    class Meta:
        #managed = False
        db_table = 'proveedor'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["prov_nombre"]
    def __str__(self):
        return f"{self.prov_nombre}"
    
# ===============================================================================================================================