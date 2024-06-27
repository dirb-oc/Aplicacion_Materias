from django.shortcuts import render, redirect
from .models import *
from .form import *

def Inicio(request):
    
    total_creditos = Semestre.Creditos_T()
    creditos_A = Semestre.Creditos_Aprobados()
    porcentaje_Creditos = int(creditos_A * 100 / total_creditos) if total_creditos != 0 else 0
    
    total_materias = Semestre.Materias_T()
    Materias_A = Semestre.Materias_Aprobados()
    porcentaje_Materias = int((Materias_A * 100 / total_materias) if total_materias != 0 else 0)

    promedio_Carrera_F = Materia.Promedio_Carrera_F()
    porcentaje_Promedio_F = int(promedio_Carrera_F * 100 / 50) if promedio_Carrera_F != 0 else 0

    promedio_Carrera_P = Materia.Promedio_Carrera_P()
    porcentaje_Promedio_P = int(promedio_Carrera_P * 100 / 50) if promedio_Carrera_P != 0 else 0
    
    semestre_C = Semestre.objects.filter(Estado=2)

    context = {
        'Cantidad' : total_creditos,
        'C_Aprobados': creditos_A,
        'Porcentaje_Creditos': porcentaje_Creditos,
        'Mat' : total_materias,
        'M_Aprobadas': Materias_A,
        'Porcentaje_Materias': porcentaje_Materias,
        'promedio_Carrera': promedio_Carrera_F,
        'procentaje_Carrera_F': porcentaje_Promedio_F,
        'promedio_Carrera_Parcial': promedio_Carrera_P,
        'procentaje_Carrera_P': porcentaje_Promedio_P,
        'Semestre_C': semestre_C}
    
    return render(request, 'Index.html',context)

#Semestres
def Semestres(request):
    Semestres = Semestre.objects.all()
    
    return render(request, 'Semestre.html',{'Semestres': Semestres})

def SemestreCursando(request):
    semestres_cursando = Semestre.objects.filter(Estado=2)
    materias = Materia.objects.filter(Semestre__in=semestres_cursando)

    return render(request, 'SemestreCursando.html', {'Materias': materias})

def FormularioSemestre(request):
    if request.method == 'POST':
        form = Semestreform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Formulario')
    else:
        form = Semestreform()

    return render(request, 'FormularioSemestre.html',{'form': form})

def EditarSemetre(request,Id):
    Llave = Semestre.objects.get(id=Id)
    if request.method == 'POST':
        form = Semestreform(request.POST, instance= Llave)
        if form.is_valid():
            form.save()
            return redirect('Semestres')
    else:
        form = Semestreform(instance=Llave)

    return render(request, 'FormularioSemestre.html',{'form': form})

def AceptarSemestre(request,Id):
    semestre = Semestre.objects.get(id=Id)
    
    return render(request, 'Comprobacion.html',{'semestre': semestre})

def EliminarSemestre(request, Id):

    if request.method == 'POST':
        semestre = Semestre.objects.get(id=Id)
        semestre.delete()
        
        return redirect('Semestres')

#Materias
def Materias(request):
    Materias = Materia.objects.all()

    return render(request, 'Materias.html', {'Materias': Materias})

def Materias_Semestre(request, Id):
    Informacion = Semestre.objects.filter(id=Id)
    Materias = Materia.objects.filter(Semestre=Id)

    context = {
        'Informacion': Informacion,
        'Materias': Materias
    }

    return render(request, 'Materias_Semestre.html', context)

def FormularioMateria(request):
    if request.method == 'POST':
        form = Materiaform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('FormularioMateria')
    else:
        form = Materiaform()

    return render(request, 'FormularioMateria.html',{'form': form})

def EditarMateria(request,Id):
    Llave = Materia.objects.get(id=Id)
    if request.method == 'POST':
        form = Materiaform(request.POST, instance= Llave)
        if form.is_valid():
            form.save()
            return redirect('Materias')
    else:
        form = Materiaform(instance=Llave)

    return render(request, 'FormularioMateria.html',{'form': form})

def AceptarMateria(request,Id):
    Mat = Materia.objects.get(id=Id)
    
    return render(request, 'ComprobacionMateria.html',{'materia': Mat})

def EliminarMateria(request, Id):
    Mat = Materia.objects.get(id=Id)
    Mat.delete()

    return redirect('Materias')

#Notas y horario
def Notas(request, Id_Materia):
    Informacion = Materia.objects.filter(id=Id_Materia)
    Notas = Nota.objects.filter(Materia=Id_Materia)
    Clases = Horario.objects.filter(Materia=Id_Materia)
    
    context= {
        'Informacion': Informacion,
        'Notas': Notas, 
        'Id_Materia': Id_Materia, 
        'Horario':Clases
    }

    return render(request, 'Nota.html', context)

def FormularioNota(request, Id_Materia):
    cn = Nota.objects.filter(Materia = Id_Materia).count()
    cm = Materia.objects.get(id=Id_Materia).Cantidad_Notas

    if cn >= cm:
        form = 'Se ha alcanzado el maximo de notas' 
    else:
        if request.method == 'POST':
            form = Notaform(request.POST)
            if form.is_valid():
                mat = form.save(commit=False)
                mat.Materia_id = Id_Materia
                mat.save()
                return redirect('FormularioNota', Id_Materia)
        else:
            form = Notaform()

    return render(request, 'FormularioNota.html', {'form': form, 'Id_Materia': Id_Materia})

def EditarNota(request,Id):
    Llave = Nota.objects.get(id=Id)
    if request.method == 'POST':
        form = Notaform(request.POST, instance= Llave)
        if form.is_valid():
            form.save()
            return redirect('Notas', Llave.Materia.id)
    else:
        form = Notaform(instance=Llave)

    return render(request, 'Editar_Nota.html',{'form': form, 'Id_Materia': Llave.Materia.id, 'Id_Nota':Id})

def EliminarNota(request, Id):
    Mat = Nota.objects.get(id=Id)
    Mat.delete()

    return redirect('Notas', Mat.Materia.id)

def FormularioHorario(request, Id_Materia):
    if request.method == 'POST':
            form = Horarioform(request.POST)
            if form.is_valid():
                hor = form.save(commit=False)
                hor.Materia_id = Id_Materia
                hor.save()
                return redirect('FormularioHorario', Id_Materia)
    else:
        form = Horarioform()

    return render(request, 'FormularioHorario.html',{'form': form, 'Id_Materia': Id_Materia})

def EditarHorario(request,Id):
    Llave = Horario.objects.get(id=Id)
    if request.method == 'POST':
        form = Horarioform(request.POST, instance= Llave)
        if form.is_valid():
            form.save()
            return redirect('Notas', Llave.Materia.id)
    else:
        form = Horarioform(instance=Llave)

    return render(request, 'Editar_Horario.html',{'form': form, 'Id_Materia': Llave.Materia.id, 'Id_Horario':Id})

def EliminarHorario(request, Id):
    Hor = Horario.objects.get(id=Id)
    Hor.delete()

    return redirect('Notas', Hor.Materia.id)