# Generated by Django 3.2.7 on 2021-09-18 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_librarybook'),
    ]

    operations = [
        migrations.RenameField(
            model_name='librarybook',
            old_name='library_id',
            new_name='library',
        ),
    ]