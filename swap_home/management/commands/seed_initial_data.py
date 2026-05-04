import os
from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction

from swap_home.models import Tareadia, Tareaestado, Tareas
from swap_tthh.models import Departamentos, Funcionarios
from swap_porteria.models import Estadoentrada, Cobrador, Proveedor
from swap_informatica.models import (
    Backupsdia,
    Backupsestado,
    BackupsSemanaControl,
    Discos,
    InventarioinformaticaDeposito,
    InventarioinformaticaEstado,
    InventarioinformaticaCategoria,
    Tipoequipo,
    MantenimientoTipo,
    Mantenimientoestado,
)
from swap_serviciotecnico.models import Tecnicosmonto


class Command(BaseCommand):
    help = "Carga datos iniciales necesarios para usar el sistema en una base nueva."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.create_groups()
            self.create_users()
            self.create_departamentos()
            self.create_estados_generales()
            self.create_tareas_base()
            self.create_backups_base()
            self.create_inventario_base()
            self.create_equipos_base()
            self.create_mantenimiento_base()
            self.create_servicio_tecnico_base()
            self.create_demo_records()

        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados correctamente."))

    def create_groups(self):
        grupos = [
            "TTHH",
            "Informatica",
            "Porteria",
            "Tecnico",
            "ServicioTecnico",
        ]

        for nombre in grupos:
            Group.objects.get_or_create(name=nombre)

    def create_users(self):
        """
        Passwords configurables desde .env.
        Si no existen variables, usa claves simples para demo/local.
        Cambialas si vas a publicar instrucciones.
        """

        users = [
            {
                "username": "admin",
                "password": os.environ.get("DJANGO_ADMIN_PASSWORD", "admin123"),
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "SWAP",
                "is_staff": True,
                "is_superuser": True,
                "group": None,
            },
            {
                "username": "tthh",
                "password": os.environ.get("DJANGO_TTHH_PASSWORD", "tthh123"),
                "email": "tthh@example.com",
                "first_name": "Usuario",
                "last_name": "TTHH",
                "is_staff": False,
                "is_superuser": False,
                "group": "TTHH",
            },
            {
                "username": "informatica",
                "password": os.environ.get("DJANGO_INFORMATICA_PASSWORD", "informatica123"),
                "email": "informatica@example.com",
                "first_name": "Usuario",
                "last_name": "Informatica",
                "is_staff": False,
                "is_superuser": False,
                "group": "Informatica",
            },
            {
                "username": "porteria",
                "password": os.environ.get("DJANGO_PORTERIA_PASSWORD", "porteria123"),
                "email": "porteria@example.com",
                "first_name": "Usuario",
                "last_name": "Porteria",
                "is_staff": False,
                "is_superuser": False,
                "group": "Porteria",
            },
            {
                "username": "tecnico",
                "password": os.environ.get("DJANGO_TECNICO_PASSWORD", "tecnico123"),
                "email": "tecnico@example.com",
                "first_name": "Tecnico",
                "last_name": "Demo",
                "is_staff": False,
                "is_superuser": False,
                "group": "Tecnico",
            },
            {
                "username": "serviciotecnico",
                "password": os.environ.get("DJANGO_SERVICIO_TECNICO_PASSWORD", "servicio123"),
                "email": "serviciotecnico@example.com",
                "first_name": "Usuario",
                "last_name": "Servicio Tecnico",
                "is_staff": False,
                "is_superuser": False,
                "group": "ServicioTecnico",
            },
        ]

        for data in users:
            password = data.pop("password")
            group_name = data.pop("group")

            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults=data,
            )

            if created:
                user.set_password(password)
                user.save()

            if group_name:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)

    def create_departamentos(self):
        departamentos = [
            "General",
            "TTHH",
            "Informatica",
            "Porteria",
            "Tecnico",
            "ServicioTecnico",
        ]

        for nombre in departamentos:
            Departamentos.objects.get_or_create(
                dpto_nombre=nombre,
                defaults={
                    "dpto_estatus": "activo",
                    "dpto_nombreorganizacion": "SWAP",
                },
            )

    def create_estados_generales(self):
        for estado in ["Pendiente⚠️", "Finalizado✅", "Cancelar❌"]:
            Estadoentrada.objects.get_or_create(ee_estado=estado)

        for estado in ["Pendiente⚠️", "Finalizado✅", "Cancelar❌", "General"]:
            Tareaestado.objects.get_or_create(te_estado=estado)

        for dia in [
            "General",
            "Lunes",
            "Martes",
            "Miercoles",
            "Jueves",
            "Viernes",
            "Sabado",
            "Domingo",
        ]:
            Tareadia.objects.get_or_create(td_dia=dia)

    def create_tareas_base(self):
        general = Departamentos.objects.get(dpto_nombre="General")
        tthh = Departamentos.objects.get(dpto_nombre="TTHH")
        informatica = Departamentos.objects.get(dpto_nombre="Informatica")

        estado_general = Tareaestado.objects.get(te_estado="General")
        estado_pendiente = Tareaestado.objects.get(te_estado="Pendiente⚠️")
        dia_general = Tareadia.objects.get(td_dia="General")
        lunes = Tareadia.objects.get(td_dia="Lunes")

        tareas = [
            {
                "tarea_titulo": "Revisar pendientes generales",
                "tarea_descripcion": "Tarea base visible para paneles generales.",
                "tarea_dpto": general,
                "tarea_te": estado_general,
                "tarea_td": dia_general,
            },
            {
                "tarea_titulo": "Actualizar datos de funcionarios",
                "tarea_descripcion": "Tarea base para TTHH.",
                "tarea_dpto": tthh,
                "tarea_te": estado_pendiente,
                "tarea_td": lunes,
            },
            {
                "tarea_titulo": "Revisar backups semanales",
                "tarea_descripcion": "Tarea base para Informatica.",
                "tarea_dpto": informatica,
                "tarea_te": estado_pendiente,
                "tarea_td": lunes,
            },
        ]

        for data in tareas:
            Tareas.objects.get_or_create(
                tarea_titulo=data["tarea_titulo"],
                defaults=data,
            )

    def create_backups_base(self):
        for dia in ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]:
            Backupsdia.objects.get_or_create(bd_dia=dia)

        for estado in ["Pendiente⏳", "Finalizado✅", "Inactivo❌"]:
            Backupsestado.objects.get_or_create(be_estado=estado)

        for disco in ["Disco Local", "Disco Externo", "Servidor"]:
            Discos.objects.get_or_create(disco_nombre=disco)

        BackupsSemanaControl.objects.get_or_create(
            id=1,
            defaults={"last_week_start": date.today()},
        )

    def create_inventario_base(self):
        for deposito in ["Deposito Principal", "Soporte Tecnico", "Oficina"]:
            InventarioinformaticaDeposito.objects.get_or_create(iid_nombre=deposito)

        for estado in ["Disponible", "En uso", "Dañado", "Baja"]:
            InventarioinformaticaEstado.objects.get_or_create(iie_nombre=estado)

        for categoria in ["Mouse", "Teclado", "Cable HDMI", "Cable VGA", "Memoria RAM", "Disco SSD"]:
            InventarioinformaticaCategoria.objects.get_or_create(iic_nombre=categoria)

    def create_equipos_base(self):
        for tipo in [
            "PC",
            "Notebook",
            "UPS",
            "Impresora",
            "Router",
            "DVR",
            "Laser",
            "Scaner",
            "Rack",
            "Switch",
            "Servidor",
            "Monitor",
        ]:
            Tipoequipo.objects.get_or_create(tipe_nombre=tipo)

    def create_mantenimiento_base(self):
        for tipo in ["Preventivo", "Correctivo", "Limpieza", "Revision"]:
            MantenimientoTipo.objects.get_or_create(mt_nombre=tipo)

        for estado in ["Pendiente⚠️", "Finalizado✅", "Cancelar❌"]:
            Mantenimientoestado.objects.get_or_create(me_estado=estado)

    def create_servicio_tecnico_base(self):
        for monto in [0, 50000, 100000, 150000, 200000]:
            Tecnicosmonto.objects.get_or_create(tm_monto=monto)

    def create_demo_records(self):
        dpto_general = Departamentos.objects.get(dpto_nombre="General")

        Funcionarios.objects.get_or_create(
            fun_ci=1234567,
            defaults={
                "fun_nombres_apellidos": "Funcionario Demo",
                "fun_correo": "funcionario@example.com",
                "fun_sueldo": 0,
                "fun_cel": "0000",
                "fun_dpto": dpto_general,
                "fun_entrada": date.today(),
                "fun_estado": "activo",
            },
        )

        Cobrador.objects.get_or_create(
            cob_nombre="Cobrador Demo",
            defaults={"cob_estado": "activo"},
        )

        Proveedor.objects.get_or_create(
            prov_nombre="Proveedor Demo",
            defaults={"prov_estado": "activo"},
        )