from django.db import models
from swap_tthh.models import *
# Create your models here.
# ===============================================================================================================================
# Informatica
# --- Backup ---

class Funcionarioconequipo(models.Model):
    fce_id = models.SmallAutoField(primary_key=True)  # The composite primary key (fce_id, fce_fun_id) found, that is not supported. The first column is selected.
    fce_equipo = models.CharField(max_length=60, verbose_name="Equipo (pc/notebook)")
    fce_fun = models.ForeignKey('swap_tthh.Funcionarios', models.DO_NOTHING, verbose_name="Funcionario")
    fce_nombre_equipo = models.CharField(max_length=60, verbose_name="Nombre del Equipo")
    fce_nombre_sati = models.CharField(max_length=60, verbose_name="Nombre")
    fce_serie_sati = models.CharField(max_length=60, verbose_name="Serie")
    fce_ip = models.CharField(max_length=60, verbose_name="IP")
    fce_observaciones = models.CharField(max_length=200, blank=True, null=True, verbose_name="Observaciones")
    fce_ruta_imagen = models.CharField(max_length=255, blank=True, null=True, verbose_name="Imagen")
    fce_estado = models.CharField(max_length=60, verbose_name="Estado(activo/inactivo)")
    class Meta:
        #managed = False
        db_table = 'funcionarioconequipo'
        verbose_name = "Funcionario con Equipo"
        verbose_name_plural = "Funcionarios con Equipo"
        ordering = ["fce_fun"]
    def __str__(self):
        return f"{self.fce_fun}"        

class Backups(models.Model):
    b_id = models.AutoField(primary_key=True)  # The composite primary key (b_id, b_disco_id, b_fce_id) found, that is not supported. The first column is selected.
    b_disco = models.ForeignKey('Discos', models.DO_NOTHING, verbose_name="Disco Correspondiente")
    b_equipo = models.CharField(max_length=60, verbose_name="Equipo (pc/notebook)")
    b_nombre = models.CharField(max_length=80, verbose_name="Nombre del Backup")
    b_fce = models.ForeignKey('Funcionarioconequipo', models.DO_NOTHING, verbose_name="Funcionario")
    b_estado = models.CharField(max_length=45, verbose_name="Estado(activo/inactivo)")
    class Meta:
        #managed = False
        db_table = 'backups'
        verbose_name = "Backup"
        verbose_name_plural = "Backups"
        ordering = ["b_disco"]
    def __str__(self):
        return f"{self.b_fce} | {self.b_disco} | {self.b_equipo}"

class BackupsSemanaControl(models.Model):
    """
    Singleton de control: guarda el lunes (inicio ISO) de la última semana reseteada.
    """
    last_week_start = models.DateField()

    def __str__(self):
        return f"Último reset: {self.last_week_start}"

class Backupsdia(models.Model):
    bd_id = models.AutoField(primary_key=True)
    bd_dia = models.CharField(max_length=45, verbose_name="Dia del Backup")
    class Meta:
        #managed = False
        db_table = 'backupsdia'
        verbose_name = "Dia del Backup"
        verbose_name_plural = "Dias de los Backups"
        #ordering = ["bd_dia"]
    def __str__(self):
        return f"{self.bd_dia}"

class Backupsestado(models.Model):
    be_id = models.AutoField(primary_key=True)
    be_estado = models.CharField(max_length=45, verbose_name="Estado")
    class Meta:
        #managed = False
        db_table = 'backupsestado'
        verbose_name = "Estado del Backup"
        verbose_name_plural = "Estados de los Backups"
        ordering = ["be_estado"]
    def __str__(self):
        return f"{self.be_estado}"

class Backupshechos(models.Model):
    bh_id = models.AutoField(primary_key=True)  # The composite primary key (bh_id, bh_bp_id) found, that is not supported. The first column is selected.
    bh_fecha = models.DateField(verbose_name="Fecha del Backup")
    bh_week_start = models.DateField(verbose_name="Semana (lunes)", db_index=True)
    bh_bp = models.ForeignKey('Backupsproceso', models.DO_NOTHING, verbose_name="Backup", blank=True, null=True)
    class Meta:
        db_table = 'backupshechos'
        verbose_name = "Backup Hecho"
        verbose_name_plural = "Backups Hechos"
        ordering = ["bh_fecha"]
        constraints = [
            models.UniqueConstraint(
                fields=["bh_bp", "bh_week_start"],
                name="unique_backup_por_semana"
            )
        ]

    def __str__(self):
        return f"{self.bh_fecha} - {self.bh_bp}"

class Backupsproceso(models.Model):
    bp_id = models.SmallAutoField(primary_key=True)  # The composite primary key (bp_id, bp_bd_id, bp_b_id, bp_be_id) found, that is not supported. The first column is selected.
    bp_bd = models.ForeignKey(Backupsdia, models.DO_NOTHING, verbose_name="Dia del Backup")
    bp_b = models.ForeignKey(Backups, models.DO_NOTHING, verbose_name="Backup")
    bp_be = models.ForeignKey(Backupsestado, models.DO_NOTHING, blank=True, null=True, verbose_name="Estado")
    class Meta:
        #managed = False
        db_table = 'backupsproceso'
        verbose_name = "Backup en Proceso"
        verbose_name_plural = "Backups en Procesos"
        ordering = ["bp_bd"]
    def __str__(self):
        return f"{self.bp_b}"

class Discos(models.Model):
    disco_id = models.AutoField(primary_key=True)
    disco_nombre = models.CharField(max_length=60, verbose_name="Nombre del Disco")
    class Meta:
        #managed = False
        db_table = 'discos'
        verbose_name = "Disco"
        verbose_name_plural = "Discos"
        ordering = ["disco_nombre"]
    def __str__(self):
        return f"{self.disco_nombre}"

# --- Inventario Informatica ---

class Inventarioinformatica(models.Model):
    ii_id = models.AutoField(primary_key=True)  # The composite primary key (ii_id, ii_iic_id, ii_iid_id, ii_iie_id) found, that is not supported. The first column is selected.
    ii_cantidad = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cantidad")
    ii_descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripcion")
    ii_fecha = models.DateField(blank=True, null=True, verbose_name="Fecha")
    ii_iic = models.ForeignKey('InventarioinformaticaCategoria', models.DO_NOTHING, verbose_name="Articulo")
    ii_iid = models.ForeignKey('InventarioinformaticaDeposito', models.DO_NOTHING, verbose_name="Deposito")
    ii_iie = models.ForeignKey('InventarioinformaticaEstado', models.DO_NOTHING, verbose_name="Estado")
    ii_ruta_imagen = models.CharField(max_length=255, blank=True, null=True, verbose_name="Imagen")
    class Meta:
        #managed = False
        db_table = 'inventarioinformatica'
        verbose_name = "Item Informatica"
        verbose_name_plural = "Inventario Informatica"
        ordering = ["ii_iid"]
    def __str__(self):
        return f"{self.ii_iic} - {self.ii_descripcion} ({self.ii_cantidad})"

class InventarioinformaticaCategoria(models.Model):
    iic_id = models.SmallAutoField(primary_key=True)
    iic_nombre = models.CharField(max_length=150, verbose_name="Articulo")
    class Meta:
        #managed = False
        db_table = 'inventarioinformatica_categoria'
        verbose_name = "Categoria (inventario)"
        verbose_name_plural = "Categorias (inventario)"
        ordering = ["iic_nombre"]
    def __str__(self):
        return f"{self.iic_nombre}"

class InventarioinformaticaDeposito(models.Model):
    iid_id = models.AutoField(primary_key=True)
    iid_nombre = models.CharField(max_length=60, verbose_name="Deposito")
    class Meta:
       # managed = False
        db_table = 'inventarioinformatica_deposito'
        verbose_name = "Deposito (inventario)"
        verbose_name_plural = "Depositos (inventario)"
        ordering = ["iid_nombre"]
    def __str__(self):
        return f"{self.iid_nombre}"

class InventarioinformaticaEstado(models.Model):
    iie_id = models.AutoField(primary_key=True)
    iie_nombre = models.CharField(max_length=50, verbose_name="Estado")
    class Meta:
       # managed = False
        db_table = 'inventarioinformatica_estado'
        verbose_name = "Estado (inventario)"
        verbose_name_plural = "Estados (inventario)"
        ordering = ["iie_nombre"]
    def __str__(self):
        return f"{self.iie_nombre}"

# class Equipos(models.Model):
#     eq_id = models.SmallAutoField(primary_key=True)
#     eq_tipe = models.ForeignKey('Tipoequipo', models.DO_NOTHING,verbose_name="Tipo de Equipo")
#     eq_numdeserie = models.CharField(max_length=45, verbose_name="Numero de Serie")
#     eq_dpto = models.ForeignKey(Departamentos, models.DO_NOTHING, verbose_name="Departamento")
#     eq_usuario = models.CharField(max_length=60, blank=True, null=True, verbose_name="Usuario")
#     eq_contrasenna = models.CharField(max_length=45, blank=True, null=True, verbose_name="Contraseña")
#     eq_marca = models.CharField(max_length=45, blank=True, null=True, verbose_name="Marca")
#     eq_modelo = models.CharField(max_length=45, blank=True, null=True, verbose_name="Modelo")
#     eq_marcamonitor = models.CharField(max_length=45, blank=True, null=True, verbose_name="Marca del Monitor")
#     eq_pulgadamonitor = models.CharField(max_length=45, blank=True, null=True, verbose_name="Pulgadas del Monitor")
#     eq_placamadre = models.CharField(max_length=45, blank=True, null=True, verbose_name="Placa Madre")
#     eq_grafica = models.CharField(max_length=45, blank=True, null=True, verbose_name="Tarjeta Grafica")
#     eq_discoduro = models.CharField(max_length=45, blank=True, null=True, verbose_name="Disco Duro")
#     eq_lectordisco = models.CharField(max_length=45, blank=True, null=True, verbose_name="Lector de Disco")
#     eq_audio = models.CharField(max_length=45, blank=True, null=True, verbose_name="Audio")
#     eq_sistemop = models.CharField(max_length=45, blank=True, null=True, verbose_name="Sistema Operativo")
#     class Meta:
#         #managed = False
#         db_table = 'equipos'
#         verbose_name = "Equipo"
#         verbose_name_plural = "Equipos"
#         ordering = ["eq_tipe"]
#     def __str__(self):
#         return  f"{self.eq_id} {self.eq_tipe} {self.eq_usuario} {self.eq_dpto}"
from django.db import models

class Equipos(models.Model):
    eq_id = models.SmallAutoField(primary_key=True)
    eq_tipe = models.ForeignKey('Tipoequipo', models.DO_NOTHING, verbose_name="Tipo de Equipo")
    eq_numdeserie = models.CharField(max_length=45, verbose_name="Numero de Serie")
    eq_dpto = models.ForeignKey(Departamentos, models.DO_NOTHING, verbose_name="Departamento")
    eq_usuario = models.CharField(max_length=60, blank=True, null=True, verbose_name="Usuario")
    eq_contrasenna = models.CharField(max_length=45, blank=True, null=True, verbose_name="Contraseña")
    eq_marca = models.CharField(max_length=45, blank=True, null=True, verbose_name="Marca")
    eq_modelo = models.CharField(max_length=45, blank=True, null=True, verbose_name="Modelo")
    eq_marcamonitor = models.CharField(max_length=45, blank=True, null=True, verbose_name="Marca del Monitor")
    eq_pulgadamonitor = models.CharField(max_length=45, blank=True, null=True, verbose_name="Pulgadas del Monitor")
    eq_placamadre = models.CharField(max_length=45, blank=True, null=True, verbose_name="Placa Madre")
    eq_grafica = models.CharField(max_length=45, blank=True, null=True, verbose_name="Tarjeta Grafica")
    eq_discoduro = models.CharField(max_length=45, blank=True, null=True, verbose_name="Disco Duro")
    eq_lectordisco = models.CharField(max_length=45, blank=True, null=True, verbose_name="Lector de Disco")
    eq_audio = models.CharField(max_length=45, blank=True, null=True, verbose_name="Audio")
    eq_sistemop = models.CharField(max_length=45, blank=True, null=True, verbose_name="Sistema Operativo")

    # 🔽 Nuevos campos agregados(me olvide de agregar el prefijo "eq_")
    nombre = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Nombre")
    nombre_equipo = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Nombre del Equipo")
    ip = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Dirección IP")
    responsable = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Responsable")
    conexion_monitor = models.CharField(max_length=70, blank=True, null=True, default="-", verbose_name="Conexión del Monitor")
    ram = models.CharField(max_length=50, blank=True, null=True, default="-", verbose_name="RAM")
    cpu = models.CharField(max_length=50, blank=True, null=True, default="-", verbose_name="CPU")
    mouse = models.CharField(max_length=80, blank=True, null=True, default="-", verbose_name="Mouse")
    teclado = models.CharField(max_length=80, blank=True, null=True, default="-", verbose_name="Teclado")
    accesorios = models.CharField(max_length=200, blank=True, null=True, default="-", verbose_name="Accesorios")
    office = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Office")
    antiviruz = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Antivirus")
    thunderbird = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Thunderbird")
    programas = models.CharField(max_length=100, blank=True, null=True, default="-", verbose_name="Programas")
    #programas = models.ImageField(upload_to='programas/', blank=True, null=True, verbose_name="Captura de Programas")
    class Meta:
        db_table = 'equipos'
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ["eq_tipe"]

    def __str__(self):
        return f"{self.eq_id} {self.eq_tipe} {self.eq_usuario} {self.eq_dpto}"


class Tipoequipo(models.Model):
    tipe_id = models.AutoField(primary_key=True)
    tipe_nombre = models.CharField(max_length=100, verbose_name="Tipo de Equipo")
    class Meta:
        #managed = False
        db_table = 'tipoequipo'
        verbose_name = "Tipo de Equipo"
        verbose_name_plural = "Tipos de Equipos"
        ordering = ["tipe_nombre"]
    def __str__(self):
        return f"{self.tipe_nombre}"
    
# --- Mantenimiento ---
    
class Mantenimiento(models.Model):
    m_id = models.AutoField(primary_key=True)
    m_fecha = models.DateField(verbose_name="Fecha del Mantenimiento")
    m_mt = models.ForeignKey('MantenimientoTipo', models.DO_NOTHING, verbose_name="Tipo de Mantenimiento")
    m_eq = models.ForeignKey(Equipos, models.DO_NOTHING,verbose_name="Equipo")
    m_responsable = models.CharField(max_length=60, verbose_name="Responsable")
    class Meta:
        #managed = False
        db_table = 'mantenimiento'
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ["m_fecha"]
    def __str__(self):
        return f"{self.m_eq} - {self.m_fecha} - {self.m_mt} - {self.m_responsable}"

class MantenimientoTipo(models.Model):
    mt_id = models.AutoField(primary_key=True)
    mt_nombre = models.CharField(max_length=70, verbose_name="Tipo de Mantenimiento")
    class Meta:
       # managed = False
        db_table = 'mantenimiento_tipo'
        verbose_name = "Tipo de Mantenimiento"
        verbose_name_plural = "Tipos de Mantenimientos"
        ordering = ["mt_nombre"]
    def __str__(self):
        return f"{self.mt_nombre}"

class Mantenimientocalendario(models.Model):
    mc_id = models.SmallAutoField(primary_key=True)
    mc_fecha = models.DateField(verbose_name="Fecha a Realizar")
    mc_mt = models.ForeignKey(MantenimientoTipo, models.DO_NOTHING, verbose_name="Tipo de Mantenimiento")
    mc_eq = models.ForeignKey(Equipos, models.DO_NOTHING, verbose_name="Equipo")
    mc_me = models.ForeignKey('Mantenimientoestado', models.DO_NOTHING, verbose_name="Estado")
    class Meta:
        #managed = False
        db_table = 'mantenimientocalendario'
        verbose_name = "Fecha de Mantenimiento"
        verbose_name_plural = "Fechas de Mantenimientos"
        ordering = ["mc_fecha"]
    def __str__(self):
        return f"{self.mc_eq} - {self.mc_fecha} - {self.mc_mt}"

class Mantenimientoestado(models.Model):
    me_id = models.AutoField(primary_key=True)
    me_estado = models.CharField(max_length=60, verbose_name="Estado de Mantenimiento")
    class Meta:
        #managed = False
        db_table = 'mantenimientoestado'
        verbose_name = "Estado de Mantenimiento"
        verbose_name_plural = "Estados de Mantenimientos"
        ordering = ["me_estado"]
    def __str__(self):
        return f"{self.me_estado}"

# ===============================================================================================================================