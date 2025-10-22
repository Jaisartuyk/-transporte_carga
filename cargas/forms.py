from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Vehiculo, Envio

# 🔹 Crear conductores
class ConductorForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "first_name", "last_name", "telefono", "documento", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = "conductor"
        if commit:
            user.save()
        return user


# 🔹 Crear vehículos


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ["placa", "marca", "modelo", "anio", "capacidad_toneladas", "conductor", "estado"]
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select"}),  # Menú desplegable
            "placa": forms.TextInput(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "anio": forms.NumberInput(attrs={"class": "form-control"}),
            "capacidad_toneladas": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "conductor": forms.Select(attrs={"class": "form-select"}),
        }



# 🔹 Crear envíos
class EnvioForm(forms.ModelForm):
    class Meta:
        model = Envio
        fields = ["numero_guia", "cliente", "vehiculo", "origen", "destino", "estado"]
