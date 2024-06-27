# Generated by Django 5.0.3 on 2024-05-27 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Categoria', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(max_length=25)),
                ('Estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Universidad.estados')),
            ],
        ),
    ]
