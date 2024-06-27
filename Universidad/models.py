from django.db import models
from django.db.models import Avg, Sum
from datetime import timedelta, datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Estados(models.Model):
    Categoria = models.CharField(max_length=25)

    def __str__(self):
        return self.Categoria

class Semestre(models.Model):
    Nombre = models.CharField(max_length=25)
    Estado = models.ForeignKey(Estados, on_delete=models.CASCADE, default=1)
    Inicio = models.DateField()
    Fin = models.DateField()

    def __str__(self):
        return self.Nombre
    
    @classmethod
    def Creditos_T(cls):
        return cls.objects.aggregate(total_creditos=Sum('materia__Creditos'))['total_creditos'] or 0
    
    @classmethod
    def Creditos_Aprobados(cls):
        return Materia.objects.filter(Termino=True).aggregate(total_creditos=Sum('Creditos'))['total_creditos'] or 0

    @classmethod
    def Materias_T(cls):
        return Materia.objects.count()
    
    @classmethod
    def Materias_Aprobados(cls):
        return Materia.objects.filter(Termino=True).count()

    def Creditos_S(self):
        creditos = (self.materia_set.aggregate(suma=Sum('Creditos'))['suma'])
        if creditos==0 or creditos is None:
            return 0
        else:
            return creditos
 
    def Promedio_m(self):
        materias = self.materia_set.all()
        sumatoria = sum(materia.Promedio_Creditos_T() for materia in materias)
        if sumatoria == 0 or self.Creditos_S() ==0:
            return 0
        else:
            return int(sumatoria/ self.Creditos_S())

    def Promedio_p(self):
        materias = self.materia_set.all()
        sumatoria = sum(materia.Promedio_Creditos_P() for materia in materias)
        if sumatoria == 0 or self.Creditos_S() ==0:
            return 0
        else:
            return int(sumatoria/ self.Creditos_S())
        
    def Clases_Semestre(self):
        return sum(materia.Clases_Materia() for materia in self.materia_set.all())

class Materia(models.Model):
    Nombre = models.CharField(max_length=35)
    Semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    Cantidad_Notas = models.IntegerField()
    Creditos = models.IntegerField()
    Minimo_A = models.IntegerField()
    Termino = models.BooleanField(default=False)

    def __str__(self):
        return self.Nombre
    
    @classmethod
    def Promedio_Carrera_F(cls):
        total_creditos = Semestre.Creditos_T()
        materias = cls.objects.all()

        if total_creditos == 0:
            return 0

        promedio_carrera = 0

        for materia in materias:
            promedio_notas = materia.Promedio_Total()
            porcentaje_creditos = (materia.Creditos / total_creditos) * 100
            resultado_porcentual = promedio_notas * (porcentaje_creditos / 100)
            promedio_carrera += resultado_porcentual

        return int(promedio_carrera)

    @classmethod
    def Promedio_Carrera_P(cls):
        total_creditos = Semestre.Creditos_Aprobados()
        materias = cls.objects.filter(Termino=True)

        if total_creditos == 0:
            return 0

        promedio_carrera = 0

        for materia in materias:
            promedio_notas = materia.Promedio_Total()
            porcentaje_creditos = (materia.Creditos / total_creditos) * 100
            resultado_porcentual = promedio_notas * (porcentaje_creditos / 100)
            promedio_carrera += resultado_porcentual

        return int(promedio_carrera)

    def Promedio_Total(self):
        sumatoria = (self.nota_set.aggregate(suma=Sum('Calificacion'))['suma'])
        if sumatoria==0 or sumatoria is None:
            return 0
        else:
            return int(sumatoria/(self.Cantidad_Notas))
    
    def Promedio_Parcial(self):
        return int(self.nota_set.aggregate(promedio=Avg('Calificacion'))['promedio'] or 0)

    def Promedio_Creditos_T(self):
        Total = self.Promedio_Total()
        if Total == 0:
            return 0
        else:
            return Total * self.Creditos
    
    def Promedio_Creditos_P(self):
        Total = self.Promedio_Parcial()
        if Total == 0:
            return 0
        else:
            return Total * self.Creditos

    DIAS_SEMANA = {
            'lunes': 'monday',
            'martes': 'tuesday',
            'miercoles': 'wednesday',
            'jueves': 'thursday',
            'viernes': 'friday',
            'sabado': 'saturday',
            'domingo': 'sunday'
    }

    def Clases_Materia(self):
        # Obtiene las fechas de inicio y fin del semestre
        inicio = self.Semestre.Inicio
        fin = self.Semestre.Fin

        Hoy = datetime.now().date()
        
        if Hoy > inicio and Hoy < fin:
            inicio = Hoy
        elif Hoy > fin:
            return 0
       
        # Días de la semana a elegir a través de un diccionario
        dias = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0, 'saturday': 0, 'sunday': 0}

        horarios = self.horario_set.all()

        dias_clase = [self.DIAS_SEMANA[horario.Dias.Dia.lower()] for horario in horarios]

        # Bucle para determinar la cantidad de días faltantes desde el inicio hasta el fin del semestre
        while inicio <= fin:
            dia = inicio.strftime('%A').lower()
            if dia in dias:
                dias[dia] += 1
            inicio += timedelta(days=1) 

        # Contar los días de clase para esta materia
        cont = sum(dias[dia] for dia in dias_clase)

        return cont

    def Total_Notas(self):
        return self.nota_set.count()
    
    def Notas_Restantes(self):
        notas = self.Total_Notas()
        return self.Cantidad_Notas - notas

    def Promedio_Faltante(self):
        Aprobacion = self.Cantidad_Notas * self.Minimo_A
        sumatoria = self.nota_set.aggregate(suma=Sum('Calificacion'))['suma'] or 0
        if Aprobacion <= sumatoria:
            return 'A'
        else:
            notas_restantes = self.Notas_Restantes()
            if notas_restantes == 0:
                return 'R'
            else:
                return int((Aprobacion - sumatoria) / notas_restantes)
            
    def Actualizar_Estado(self):
        if self.Promedio_Total() >= self.Minimo_A:
            self.Termino = True
        else:
            self.Termino = False

class Nota(models.Model):
    Calificacion = models.IntegerField()
    Descripcion = models.CharField(max_length=50)
    Materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return self.Calificacion

class Dias(models.Model):
    Dia = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.Dia
    
class Horario(models.Model):
    Dias = models.ForeignKey(Dias, on_delete=models.CASCADE)
    Materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.Dias
    
@receiver(post_save, sender=Nota)
def actualizar_estado_materia(sender, instance, **kwargs):
    informacion = instance.Materia
    informacion.Actualizar_Estado()
    informacion.save()

@receiver(post_delete, sender=Nota)
def actualizar_estado_materia(sender, instance, **kwargs):
    informacion = instance.Materia
    informacion.Actualizar_Estado()
    informacion.save()