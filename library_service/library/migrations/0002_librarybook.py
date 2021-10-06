# Generated by Django 3.2.7 on 2021-09-18 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.BigIntegerField()),
                ('count', models.IntegerField()),
                ('library_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.library')),
            ],
        ),
    ]