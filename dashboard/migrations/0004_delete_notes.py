# Generated by Django 4.2.2 on 2023-06-18 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_notes_title'),
    ]

    operations = [
        migrations.DeleteModel(
            name='notes',
        ),
    ]
