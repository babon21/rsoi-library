# Generated by Django 3.2.7 on 2021-09-26 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='admin', max_length=30),
            preserve_default=False,
        ),
    ]
