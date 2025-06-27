from django.db import models
from swap_porteria.models import *
from swap_tthh.models import *
# Create your models here.


# ===============================================================================================================================
# ===============================================================================================================================
# ===============================================================================================================================
# Login

# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         #managed = False
#         db_table = 'auth_group'

# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         #managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)

# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         #managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)

# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         #managed = False
#         db_table = 'auth_user'

# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         #managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)

# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         #managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)

# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         #managed = False
#         db_table = 'django_admin_log'

# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         #managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)

# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         #managed = False
#         db_table = 'django_migrations'

# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         #managed = False
#         db_table = 'django_session'
   
# ===============================================================================================================================
# ===============================================================================================================================
# ===============================================================================================================================

# Generales

    
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


