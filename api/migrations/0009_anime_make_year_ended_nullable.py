# Generated by Django 2.0.8 on 2018-12-15 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_make_year_fields_positive_small_integers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='year_ended',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
