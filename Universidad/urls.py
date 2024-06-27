from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.Inicio, name='Inicio'),

    #Semestre
    path('semestre', views.Semestres, name='Semestres'),
    path('sc', views.SemestreCursando, name='SemestresCurso'),
    path('fs', views.FormularioSemestre, name='Formulario'),
    path('es/<int:Id>', views.EditarSemetre, name='Editar'),
    path('cs/<int:Id>', views.AceptarSemestre, name='Comprobante'),
    path('ds/<int:Id>', views.EliminarSemestre, name='Eliminar'),
    
    #Materia
    path('materias', views.Materias, name='Materias'),
    path('materia/<int:Id>', views.Materias_Semestre, name='MateriasSemestre'),
    path('fm', views.FormularioMateria, name='FormularioMateria'),
    path('em/<int:Id>', views.EditarMateria, name='EditarMateria'),
    path('cm/<int:Id>', views.AceptarMateria, name='ComprobanteMateria'),
    path('dm/<int:Id>', views.EliminarMateria, name='EliminarMateria'),

    #Notas y Horario
    path('nota/<int:Id_Materia>', views.Notas, name='Notas'),
    path('fn/<int:Id_Materia>', views.FormularioNota, name='FormularioNota'),
    path('fh/<int:Id_Materia>', views.FormularioHorario, name='FormularioHorario'),
    path('en/<int:Id>', views.EditarNota, name='EditarNota'),
    path('dn/<int:Id>', views.EliminarNota, name='EliminarNota'),
    path('eh/<int:Id>', views.EditarHorario, name='EditarHorario'),
    path('dh/<int:Id>', views.EliminarHorario, name='EliminarHorario'),

]
