# Generated by Django 2.0.8 on 2018-12-15 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_character'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
