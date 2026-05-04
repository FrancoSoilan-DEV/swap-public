from swap_informatica.models import *


def crear_mantenimiento_desde_calendario(calendario: Mantenimientocalendario, responsable: str):
    return Mantenimiento.objects.create(
        m_fecha=calendario.mc_fecha,
        m_mt=calendario.mc_mt,
        m_eq=calendario.mc_eq,
        m_responsable=responsable
    )
