# Generated by Django 3.2.7 on 2021-10-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_takenbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='takenbook',
            name='expire_date',
            field=models.DateTimeField(default='2013-03-30'),
            preserve_default=False,
        ),
    ]