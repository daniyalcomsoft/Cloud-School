# Generated by Django 4.1.1 on 2022-12-12 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolsession',
            name='SessionEnd',
            field=models.DateField(blank=True, null=True, verbose_name='Session End'),
        ),
        migrations.AlterField(
            model_name='schoolsession',
            name='SessionStart',
            field=models.DateField(blank=True, null=True, verbose_name='Session Start'),
        ),
    ]
