# Generated by Django 3.1.3 on 2020-11-21 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start', '0003_auto_20201120_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activateprofile',
            name='code',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
