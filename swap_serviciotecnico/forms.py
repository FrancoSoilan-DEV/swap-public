from django import forms 
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *

class MontoForm(forms.ModelForm):
    class Meta:
        model = Tecnicosmonto
        fields = ["tm_monto"]
        labels = {
            "tm_monto":"Monto",
        }