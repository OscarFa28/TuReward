# Generated by Django 4.2.16 on 2024-11-30 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminPanel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birthday',
        ),
    ]