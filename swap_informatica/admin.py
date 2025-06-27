from django.contrib import admin
from swap_informatica.models import *
# Register your models here.

admin.site.register(Backups)
admin.site.register(Backupsdia)
admin.site.register(Backupsestado)
admin.site.register(Backupsproceso)
admin.site.register(Backupshechos)
admin.site.register(Discos)

admin.site.register(Funcionarioconequipo)

admin.site.register(Inventarioinformatica)
admin.site.register(InventarioinformaticaCategoria)
admin.site.register(InventarioinformaticaDeposito)
admin.site.register(InventarioinformaticaEstado)
admin.site.register(Tipoequipo)
admin.site.register(Equipos)

admin.site.register(MantenimientoTipo)
admin.site.register(Mantenimiento)
admin.site.register(Mantenimientocalendario)
admin.site.register(Mantenimientoestado)