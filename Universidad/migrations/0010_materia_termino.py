# Generated by Django 5.0.3 on 2024-06-10 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Universidad', '0009_alter_nota_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='Termino',
            field=models.BooleanField(default=False),
        ),
    ]
