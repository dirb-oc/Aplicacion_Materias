# Generated by Django 5.0.3 on 2024-05-29 02:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Universidad', '0006_alter_materia_minimo_a'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dias',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dia', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Dias', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Universidad.dias')),
                ('Materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Universidad.materia')),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Calificacion', models.IntegerField()),
                ('Materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Universidad.materia')),
            ],
        ),
    ]
