from django.db import models

# Create your models here.
# --- TTHH ---
class Departamentos(models.Model):
    dpto_id = models.SmallAutoField(primary_key=True)
    dpto_nombre = models.CharField(max_length=70, verbose_name="Nombre del Departamento")
    dpto_estatus = models.CharField(max_length=45, verbose_name="Estatus del Departamento")
    dpto_nombreorganizacion = models.CharField(max_length=70, verbose_name="Nombre de la Organizacion")
    class Meta:
        #managed = False
        db_table = 'departamentos'
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["dpto_nombre"]
    def __str__(self):
        return f"{self.dpto_nombre}"

class Funcionarios(models.Model):
    fun_id = models.AutoField(primary_key=True)  # The composite primary key (fun_id, fun_dpto_id) found, that is not supported. The first column is selected.
    fun_ci = models.PositiveBigIntegerField(verbose_name="Cedula de Identidad")
    fun_nombres_apellidos = models.CharField(max_length=220, verbose_name="Nombres y Apellidos")
    fun_correo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Correo Electronico")
    fun_sueldo = models.BigIntegerField(verbose_name="Salario")
    fun_cel = models.CharField(max_length=30, verbose_name="Numero de Celular")
    fun_dpto = models.ForeignKey(Departamentos, models.DO_NOTHING, verbose_name="Departamento")
    fun_entrada = models.DateField(verbose_name="Fecha de Entrada a la Empresa")
    fun_salida = models.DateField(blank=True, null=True, verbose_name="Fecha de Salida de la Empresa")
    fun_estado = models.CharField(max_length=45, verbose_name="Estado(activo/inactivo)")
    class Meta:
        #managed = False
        db_table = 'funcionarios'
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"
        ordering = ["fun_nombres_apellidos"]
    def __str__(self):
        return f"{self.fun_nombres_apellidos}"

class Telefonosinternos(models.Model):
    ti_id = models.SmallAutoField(primary_key=True)  # The composite primary key (ti_id, ti_fun_id) found, that is not supported. The first column is selected.
    ti_numero = models.PositiveSmallIntegerField(verbose_name="Numero de Telfefono Interno")
    ti_fun = models.ForeignKey(Funcionarios, models.DO_NOTHING, verbose_name="Funcionario")
    class Meta:
        #managed = False
        db_table = 'telefonosinternos'
        verbose_name = "Telefono Interno"
        verbose_name_plural = "Telefonos Internos"
        ordering = ["ti_numero"]
    def __str__(self):
        return f"{self.ti_numero} - {self.ti_fun}"