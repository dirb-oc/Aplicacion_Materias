from django import forms
from .models import *

class Semestreform(forms.ModelForm):

    class Meta:
        model = Semestre
        fields = '__all__'

        widgets = {
            'Inicio': forms.DateInput(attrs={'type': 'date'}),
            'Fin': forms.DateInput(attrs={'type': 'date'}),
        }

class Materiaform(forms.ModelForm):

    class Meta:
        model = Materia
        fields = '__all__'
        exclude = ['Termino']

class Notaform(forms.ModelForm):

    class Meta:
        model = Nota
        fields = '__all__'
        exclude = ['Materia']

class Horarioform(forms.ModelForm):

    class Meta:
        model = Horario
        fields = '__all__'
        exclude = ['Materia']