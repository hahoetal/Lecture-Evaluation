# Generated by Django 3.2.3 on 2021-05-19 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opensemester',
            name='lectureId',
        ),
        migrations.DeleteModel(
            name='Lectures',
        ),
        migrations.DeleteModel(
            name='OpenSemester',
        ),
    ]
