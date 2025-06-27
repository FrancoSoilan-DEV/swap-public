from django import forms 
from swap_home.models import *
import datetime
from swap_home.models import *
from swap_informatica.models import *
from swap_porteria.models import *
from swap_serviciotecnico.models import *
from swap_tecnico.models import *
from swap_tthh.models import *
# Entrada de Funcionarios
class EntradaFuncionario(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ["e_fecha","e_entrada","e_fun","e_comentario"]
        labels = {
            'e_fecha': 'Fecha',
            'e_entrada': 'Entrada',
            'e_fun': 'Funcionario',
            'e_comentario':'Comentario'
        }
        widgets = {
            'e_fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',  # Clase opcional para consistencia
                },
                format='%Y-%m-%d'
            ),
            'e_entrada': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'e_comentario': forms.Textarea(attrs={
                'class': 'form-control',  # Asegura consistencia
                'rows': 4,
                'placeholder': 'Opcional...',
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fecha del dia
        if not self.fields['e_fecha'].initial:
            self.fields['e_fecha'].initial = datetime.date.today()
        #  Solo funcionarios activos
        self.fields['e_fun'].queryset = Funcionarios.objects.filter(fun_estado__iexact='activo').order_by('fun_nombres_apellidos')

# Entrada de Cobradores
class EntradaCobrador(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ["e_fecha", "e_entrada", "e_cob", "e_comentario"]
        labels = {
            'e_fecha': 'Fecha',
            'e_entrada': 'Entrada',
            'e_cob': 'Cobrador',
            'e_comentario': 'Comentario',
        }
        widgets = {
            'e_fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',  # Clase opcional para consistencia
                },
                format='%Y-%m-%d'
            ),
            'e_entrada': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                }
            ),
            'e_comentario': forms.Textarea(
                attrs={
                    'class': 'form-control',  # Asegura consistencia
                    'rows': 4,
                    'placeholder': 'Opcional...',
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fecha del dia
        if not self.fields['e_fecha'].initial:
            self.fields['e_fecha'].initial = datetime.date.today()
        # Filtrar los cobradores activos
        self.fields['e_cob'].queryset = Cobrador.objects.filter(cob_estado="activo")

# Entrada de Proveedores
class EntradaProveedor(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ["e_fecha","e_entrada","e_prov","e_comentario"] 
        labels = {
            'e_fecha': 'Fecha',
            'e_entrada': 'Entrada',
            'e_prov': 'Proveedor',
            'e_comentario': 'Comentario',
        }   
        widgets = {
            'e_fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',  # Clase opcional para consistencia
                },
                format='%Y-%m-%d'
            ),
            'e_entrada': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                }
            ),
            'e_comentario': forms.Textarea(
                attrs={
                    'class': 'form-control',  # Asegura consistencia
                    'rows': 4,
                    'placeholder': 'Opcional...',
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fecha del dia
        if not self.fields['e_fecha'].initial:
            self.fields['e_fecha'].initial = datetime.date.today()
            # Filtrar los cobradores activos
        self.fields['e_prov'].queryset = Proveedor.objects.filter(prov_estado="activo")
        
# Entrada de Visitas
class EntradaVisita(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ["e_fecha","e_entrada","e_visita","e_comentario"]
        labels = {
            'e_fecha': 'Fecha',
            'e_entrada': 'Entrada',
            'e_visita': 'Visita',
            'e_comentario': 'Comentario',
        }  
        widgets = {
            'e_fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',  # Clase opcional para consistencia
                },
                format='%Y-%m-%d'
            ),
            'e_entrada': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                }
            ),
            'e_visita': forms.TextInput(
                attrs={
                    'class': 'form-control',  # Para mantener la misma consistencia visual
                    'placeholder': 'Nombre de la visita',
                }
            ),
            'e_comentario': forms.Textarea(
                attrs={
                    'class': 'form-control',  # Asegura consistencia
                    'rows': 4,
                    'placeholder': 'Opcional...',
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fecha del dia
        if not self.fields['e_fecha'].initial:
            self.fields['e_fecha'].initial = datetime.date.today()
        
# Añadir Cobrador
class NewCobrador(forms.ModelForm):
    class Meta:
        model = Cobrador
        fields = ["cob_nombre"]
        labels = {
            'cob_nombre':'Nombre',
            'cob_estado':'Estado',
        }
        widgets = {
            'cob_nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre del Cobrador',
                }
            ),
        }
        
# Eliminar un Cobrador
class EliminarCobrador(forms.Form):
    cobrador = forms.ModelChoiceField(
        queryset=Cobrador.objects.filter(cob_estado='activo'),
        label="Seleccionar Cobrador",
        empty_label="(Seleccione un cobrador)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
# Añadir Proveedor
class NewProveedor(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["prov_nombre"]
        labels = {
            'prov_nombre':'Nombre',
            'prov_estado':'Estado',
        }
        widgets = {
            'prov_nombre': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre del Proveedor',
                }
            ),
        }
        
# Eliminar un Proveedor
class EliminarProveedor(forms.Form):
    cobrador = forms.ModelChoiceField(
        queryset=Proveedor.objects.filter(prov_estado='activo'),
        label="Seleccionar Proveedor",
        empty_label="(Seleccione un Proveedor)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )